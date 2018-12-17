from collections import defaultdict 
import pysrt 
import os
from tqdm import tqdm
import spacy
from operator import itemgetter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from collections import namedtuple
from collections import defaultdict 
import pysrt 
import os
from tqdm import tqdm
import spacy
import re
from collections import namedtuple
from matplotlib import pyplot as plt
from operator import itemgetter
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import NullFormatter
from IPython.core.display import HTML, display

import modules_comp_journ as lib
import file_parsing as files
import lexicon as lex
import printing as pn

#this file contains topic modelling, sentiment analysis, lexicon generation functions
#the functions that end in '_transcripts' are for functions in the transcripts format of
#the internet archive and the functions taht ened in '_text' are for plain text.

#takes in an array file and returns aan array of lemmatized files
def createLemmatizedTranscript(full_flat_transcript):
    nlp = spacy.load('en_core_web_sm', disable=['parser','ner'])
    i = 0
    max_index = len(full_flat_transcript) - 1 
    for t_file in nlp.pipe(tqdm(full_flat_transcript), n_threads = 4, batch_size = 100): #reduce batch size if load is too much
        lem_flat_transcript = ''
        for token in t_file: 
            lem_flat_transcript += token.lemma_ + ' '
        full_flat_transcript[i] = lem_flat_transcript
        i += 1   
    return full_flat_transcript

#computes the topic score of a string based on a lexicon.
def compute_topic_score(string, topic_words):
    score = 0
    for word in string.split(' '):
        if word in topic_words:
            topic_rank = topic_words.index(word)
            if (topic_rank ==0): score += 100 # main topic word always scored at index 0
            if (topic_rank in range (1, 10)): score += 50
            if (topic_rank in range (10, 20)): score += 40
            if (topic_rank in range (20, 30)): score += 30
            if (topic_rank in range (30, 40)): score += 20
            if (topic_rank in range (40, len(topic_words) - 1)): score += 10
    return score

# takes in a string and returns its sentiment score
def compute_sent_score(string):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = 0
    for word in string.split(' '):
        sentiment_score += analyzer.polarity_scores(word)['compound']
    return sentiment_score

# given a lexicon of right-leaning words and a lexicon of left-leaning
# words the function returns a bias score. A positive score indicates 
# left leaning bias and negative score indicates left leaning bias.

def compute_bias_score(string, right_lexicon, left_lexicon):
    left_score = 0
    last_word = ''
    last_last_word = ''
    num_words = 0
    
    for word in string.split(' '):
        num_words += 1
        two_gram = last_word + ' ' + word
        three_gram = last_last_word + ' ' + two_gram        
        
        for lex_word in right_lexicon:
            if word == lex_word or two_gram == lex_word or three_gram == lex_word:
                left_score -=1
    
        for lex_word in left_lexicon:
            if word == lex_word or two_gram == lex_word or three_gram == lex_word:
                left_score +=1
        
    last_last_word = last_word
    last_word = word

    return left_score

#helper funtion that filters segments whose topic score exceeds a certain threshold.
def get_filtered_scores(segments, lexicon, indexes, score_threshold):
    i = 0
    scores = [] 
    for segment in segments:
        score = compute_topic_score(segment, lexicon) 
        scores.append(((indexes[i]), score))
        i = i + 1
    scores_filtered = [interval for (interval, score) in scores if score > score_threshold] #took out times_raw
    return scores_filtered

# given a file and a lexicon for the desired topic, this function returns the segments on a given topic, 
# the topic score, the sentiment score, the timestamps of the each segment and a bias score given two 
#lexicons of bias. 

#PARAMETERS:
# file : file name, path: path the file is in, overlap: should be equal to 'overlap'if you want overlaping segments, 
# skip : how far apart the segments start (e.g. if we want to examine segments of length 200 and skip 70 words at a time, 
# in other words, consider segments of index 200-400, then 270-470 we would set segment_length to 200 and skip
# to 70). Score threshold is the score the topic score segment to exceeed so that it can qualify as talking about a topic,
# lexicon is the list of key-words associated with teh topic (can be outputted by the generate lexicon method), right_lexicon
# and left_lexicon are the bias lexicons. 
# returns strings that classify as talking about the segment along with other infortmation about the segments. 


def identify_segments_news_transcripts(file, path, overlap, segment_length, skip, lexicon, score_threshold, right_lexicon, left_lexicon):
    
    ar = files.create_segments_transcripts(file, path, overlap, segment_length, skip)
    
    segments = ar[0]
    times = ar[1]
    indexes = ar[2] 
    words = ar[3]
    times_raw = ar[4]
        
    scores_filtered = list(get_filtered_scores(segments, lexicon, indexes, score_threshold))
    print('len(scores_filtered): ', len(scores_filtered))
    topic_indexes_and_times = lib.combine_overlapping_intervals_transcripts(scores_filtered, times_raw)
    
    string_score_sent_timestamp = []
    Record = namedtuple('Point', ['text', 'topic_score', 'sent_score', 'bias_score', 'start_time', 'end_time', 'file'])


    for i in range(0, len(topic_indexes_and_times)): #
        new_segment = []
        seg_start = topic_indexes_and_times[i][0][0] + 1
        seg_end = topic_indexes_and_times[i][0][1] + 1
        string = ' '.join(words[seg_start : seg_end])
        topic_score = compute_topic_score(string, lexicon)
        bias_score = compute_bias_score(string, right_lexicon, left_lexicon)/len(string)
        sentiment_score = compute_sent_score(string)
        timeRange = topic_indexes_and_times[i][1]
        start_time = files.isolateTimeSegment(1, timeRange)
        end_time = files.isolateTimeSegment(2, timeRange)
        new_segment = Record(text=string, topic_score=topic_score, sent_score=sentiment_score, bias_score=bias_score, start_time=start_time,end_time=end_time,file=file)

        string_score_sent_timestamp.append(new_segment)
        
    return string_score_sent_timestamp


# given a file and a lexicon for a topic, this function returns the segments on a given topic, 
# the topic score and their seniment score. 


#PARAMETERS:
# file : file name, path: path the file is in, overlap: should be equal to 'overlap'if you want overlaping segments, 
# skip : how far apart the segments start (e.g. if we want to examine segments of length 200 and skip 70 words at a time, 
# in other words, consider segments of index 200-400, then 270-470 we would set segment_length to 200 and skip
# to 70). Score threshold is the score the topic score segment to exceeed so that it can qualify as talking about a topic,
# lexicon is the list of key-words associated with teh topic (can be outputted by the generate lexicon method) 
# returns strings that classify as talking about the segment along with other infortmation about the segments. 

def identify_segments_in_text(file, overlap, segment_length, skip, lexicon, score_threshold):
    
    ar = files.create_segments_text(file, overlap, segment_length, skip) 
    segments = ar[0]
    indexes = ar[1] 
    words = ar[2]

    scores_filtered = list(get_filtered_scores(segments, lexicon, indexes, score_threshold))
    topic_indexes = lib.combine_overlapping_intervals_text(scores_filtered)
    string_score_sent = []
    Record = namedtuple('Point', ['text', 'topic_score', 'sent_score', 'file'])

    for i in range(0, len(topic_indexes)): #
        new_segment = []
        seg_start = topic_indexes[i][0] + 1
        seg_end = topic_indexes[i][1] + 1
        string = ' '.join(words[seg_start : seg_end])
        topic_score = compute_topic_score(string, lexicon)
        sentiment_score = compute_sent_score(string)
        new_segment = Record(text=string, topic_score=topic_score, sent_score=sentiment_score, file=file)
        string_score_sent.append(new_segment)

    return string_score_sent

#takes in a file and and a topic word and returns segments in the text that are about the topic 
#as well as their topic score and their sentiment score

def topic_modelling_text(filename, topic_word):
    lexicon = lex.generate_lexicon(filename, topic_word, 100)
    segments = identify_segments_in_text(filename, 'overlap', 45, 15, lexicon, 100)
    return segments

#takes in a news transcript in the format used by the Internet Archive (and the path were the file is located)
# and and a topic word and print and returns segments in the text that are about the topic, along with their
# topic score, their sentiment score, the bias score and the timestamps of the text. The bias scre 
#is calculated by the two bias lexicons that are given.

def topic_modelling_transcript(filename, topic_word, path, right_lexicon, left_lexicon):
    lexicon = lex.generate_lexicon(filename, topic_word, 100)
    segments = identify_segments_news_transcripts(filename, path, 'overlap', 45, 15, lexicon, 100, right_lexicon, left_lexicon)
    return segments

#sample biased lexicon for political bias on the topic of immigration
immigration_right_biased_lexicon = ['abolishing', 'abused', 'acquitted', 'addressing', 'aggressive', 'alien', 'allows', 'america first', 'america is winning again', 'america safe', 'american lives', 'american worker', 'anchor baby', 'apprehend', 'apprehended', 'architect', 'arrest', 'arresting', 'assaulting', 'attack', 'avalanche', 'backfire', 'believe donald', 'benefit', 'birthright citizenship', 'blanket immunity', 'blatant', 'blocked', 'border control', 'border patrol', 'border security', 'border security', 'border wall', 'bringing diseases', 'broken', 'broken immigration', 'brutal', 'brutally', 'build a wall', 'burden', 'burglary', 'cartel', 'catch and release', 'christian identity', 'clash', 'commit', 'committing', 'common core', 'comply', 'concede', 'conceding', 'confederate', 'confuse', 'convicted', 'conviction', 'correctness', 'country illegally', 'crack', 'crackdown', 'crackdown', 'cracking', 'criminal', 'criminal aliens', 'criminal convictions', 'criminal record', 'criminality', 'crisis', 'cycle', 'dangerous', 'debt', 'defied', 'defy', 'defy', 'deliberate', 'deliberately', 'denounce', 'deportation force', 'deportee', 'diego', 'disastrous', 'disease', 'disgrace', 'diversity agenda', 'dominate', 'doubt', 'drug dealer', 'drug dealing', 'drunk', 'e-verify', 'economic burden', 'economic strain', 'efficient', 'emphasis', 'encourage', 'endless', 'enforce', 'enforcement', 'enforcing', 'entitle', 'execute', 'executive action', 'exists', 'exit', 'expedited', 'exploit', 'failed', 'failed', 'fake news', 'feds', 'felon', 'felonies', 'felony', 'financial burden', 'financial strain', 'firestorm', 'flee', 'flipped', 'flood', 'flop', 'flopping', 'food stamp', 'forces', 'foreigner', 'formulate', 'founding', 'fraud', 'free pass', 'frustrate', 'fundamental', 'gamble', 'gang members', 'gang violence', 'gangs', 'global elite', 'globalist', 'god', "god's people", 'good people', 'govern', 'great again', 'great people', 'great president', 'great wall', 'grisly', 'guard the border', 'hate', 'hiding', 'hollywood', 'human trafficking', 'hurts', 'hysterical', 'ideological certification', 'ignore', 'illegal', 'illegal alien', 'illegal immigrant', 'illegal immigration', 'illegally', 'illegals', 'illegals', 'illness', 'immigration allies', 'immigration enforcement', 'immigration laws', 'immigration plan', 'incentivizing', 'infest', 'infestation', 'influx', 'insist', 'intentionally', 'invade', 'kick them out', 'law breaker', 'lawless hoard', 'left', 'legalize', 'locally', 'low-skilled', 'lower wages', 'make america great again', 'mass', 'mass', 'mexican immigrants', 'mexico pay', "mexico sends it's people", 'mexico sends people', 'migrant caravan', 'molestation', 'moral majority', 'most dangerous', 'murder charges', 'murder trial', 'murdered', 'murderer', 'murdering', 'muslim ban', 'must leave', 'nationalist', 'native born citizen', 'no amnesty', 'no illegal', 'no immigrant', 'no legalization', 'no migrant', 'no sanctuary', 'not paying taxes', 'obama era', 'obey', 'offenders', 'offenses', 'one hundred percent', 'open borders', 'openly', 'opportunity', 'ours', 'outrage', 'overhaul', 'overrunning our country', 'passage', 'passes', 'patriot', 'pay taxes', 'permanent', 'permanently', 'permit', 'planned', 'pour', 'privileges', 'pro-amnesty', 'processed', 'prosperity', 'prosperous', 'protect', 'proud boys', 'public safety', 'quality of life', 'radical left', 'radicalize', 'raid', 'raise taxes', 'ranch', 'rape', 'raping', 'rapist', 'reasonable cost', 'recipients', 'refuse', 'refusing', 'regardless', 'reinforce', 'removal', 'removing', 'restore', 'restored', 'risks', 'rounded', 'rounding', 'scrap', 'secure', 'securing', 'security', 'send them back', 'sharia', 'shield', 'signature', 'skeptical', 'smuggle', 'smuggling', 'soft on', 'soften', 'softening', 'sovereign', 'spark', 'speak english', 'spike', 'spots', 'stab', 'staggering', 'states supreme', 'strength', 'striking', 'string', 'suppress', 'suspend immigration', 'suspending immigration', 'swear', 'taking jobs', 'taxpayer dollars', 'taxpayer money', 'terminate', 'terrorist', "they're bringing", 'thugs', 'tough', 'tough on', 'toughest', 'trafficking', 'tremendous strain', 'tribal', 'unabated', 'unemployed', 'unlawful', 'unlimited', 'unlimited immigration', 'urgent', 'vast', 'verify', 'vetting', 'viciously', 'violate', 'violence', 'violent crime', 'weak', 'welfare', 'white genocide', 'white pride', 'zero tolerance']
immigration_left_biased_lexicon = ['abide', 'abiding', 'abortion', 'accountability', 'activate', 'advisors', 'advocacy', 'aggressively', 'alienate', 'alt right', 'amnesty', 'anthem', 'anti-hispanic', 'anti-immigrant', 'anti-latino', 'anxiety', 'approach', 'assurance', 'assylum seekers', 'asylum', 'attacking', 'babies', 'baby', 'backlash', 'backwards', 'balance', 'berate', 'bitter', 'blame', 'blanket', 'bolster', 'bottom', 'cage', 'care', 'catastrophe', 'challenger', 'childhood', 'cite', 'coherent', 'compassionate', 'complicate', 'complicit', 'conflate', 'confuse', 'confusing', 'conservatism', 'constant', 'contrary', 'core', 'correlation', 'create fear', 'critically', 'crying', 'dealt', 'deceit', 'decisive', 'default', 'defiant', 'defined', 'deflect', 'demonize', 'desperate', 'detainee', 'devil', 'difference', 'dignity', 'dilemma', 'disagreement', 'disappointed', 'disapprove', 'disaster', 'disastrous', 'discord', 'discourage', 'discourse', 'discretion', 'discrimination', 'distinction', 'diverse', 'divide', 'divisive', 'documentation', 'dreamers', 'dumb', 'elevate', 'embrace', 'embraced', 'emphasize', 'employed', 'endanger', 'endorsed', 'energize', 'epidemic', 'equality', 'escalate', 'escalation', 'escort', 'established process', 'ethnic', 'exempt', 'explicitly', 'exploit', 'extreme', 'facility', 'faction', 'faithful', 'fallout', 'families apart', 'family separation', 'father', 'fear', 'fierce', 'flee', 'fleeing violence', 'forcefully', 'forefront', 'foster', 'frame', 'frustrate', 'frustrated', 'furious', 'grandparent', 'grant', 'granting', 'halt', 'hard working', 'harder', 'hardest', 'harm', 'harmful', 'hate', 'haunt', 'heavily', 'heritage', 'hiring', 'home', 'horizon', 'horror', 'hugs not walls', 'human', 'humane', 'humanitarian', 'humanity', 'hype', 'hypocrisy', 'ideological', 'ideology', 'ignorance', 'illustrate', 'imbalance', 'inability', 'inaccurate', 'incite', 'incorrect', 'inflame', 'inherit', 'inhumane', 'insane', 'interpret', 'intimidation', 'jeopardize', 'justice', 'law abiding', 'lawful', 'legalization', 'legally', 'legislative', 'legitimate', 'libertarian', 'lie', 'lies', 'live in fear', 'living in fear', 'marches', 'minors', 'misinformation', 'misrepresent', 'mobilize', 'mother', 'motivated', 'narrowly', 'nationalism', 'nationalist', 'negotiating', 'nonsense', 'normalize', 'nuance', 'obvious', 'opposite', 'optimistic', 'organizer', 'outrage', 'outreach', 'overshadow', 'overwhelming', 'pathetic', 'peak', 'peddle', 'persuade', 'pledge', 'poor', 'poorly', 'populist', 'postpone', 'practical', 'prefer', 'preference', 'preside', 'principle', 'procedures', 'productive', 'profiling', 'progress', 'progressive', 'promise', 'promising', 'proposed', 'prosperity', 'protectionist', 'proxy', 'purge', 'push', 'questionable', 'racism', 'racist', 'radical', 'ramification', 'rant', 'ratchet', 'rational', 'realistic', 'rebuild', 'rebuke', 'recognized', 'reduce', 'reform', 'reiterate', 'reject', 'religious', 'replaced', 'requires', 'research', 'resolution', 'resonate', 'responsible', 'restrictionist', 'retain', 'retreat', 'reunify', 'reunite families', 'reunited', 'revenge', 'reversal', 'right', 'rile', 'rip', 'rip children away', 'ripped', 'ripping', 'safe harbor', 'satisfy', 'scare', 'scholar', 'scholarship', 'scramble', 'script', 'seek assylum', 'seeker', 'seekers', 'seeking', 'seeking asylum', 'separations', 'sharply', 'shift', 'shithole', 'shortage', 'skilled', 'skip', 'slavery', 'slogan', 'snake', 'social justice', 'solve', 'spar', 'speculation', 'squarely', 'stark', 'status', 'stereotype', 'stoke', 'strain', 'stranger', 'studies', 'suppress', 'sweeping', 'swift', 'tear', 'terminate', 'terrify', 'terrorism', 'threats', 'tirade', 'tired', 'torture', 'toxic', 'trauma', 'traumatized', 'trickle', 'trumpism', 'tuition', 'uncertain', 'undocumented immigrants', 'undocumented migrants', 'undocumented workers', 'unfair', 'unify', 'unpopular', 'unravel', 'untrue', 'unwilling', 'urgency', 'vent', 'veto', 'viable', 'victim', 'victimized', 'violation', 'vow', 'vulgar', 'whip', 'white supremacy', 'willingness', 'workers', 'workers', 'wrong', 'xenophobic', 'false']

