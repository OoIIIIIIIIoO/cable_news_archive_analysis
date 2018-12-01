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

def non_zero_index(ar):
    i = 0
    while ( i < len(ar) and ar[i] == 0 ):
        i+=1
    return i

def get_Date(segment):
    
    string = segment.file
    ar = ''
    ar = string.split('_')
    s = ar[1]
    #k = ar[2]
    date = s[0:4] + '_' + s[4:6] + '_' + s[6:8] #+ '_' + k
    return date

def parse_file(filename, path):
    file = open(path + '/' + filename, "r")
    words = []
    stamps = []
    timestamp = 0
    i = 0   
    for line in file:
        line = line.strip()       
        #beginning of every file is a 1
        if i == 1:
            stamps.append(line)
            words.append(1)           
        if '-->' in line:
            timestamp = line
        if re.search('[a-zA-Z]', line):
            for word in line.split(' '):
                words.append(word)
                if '.' in word:
                    stamps.append(timestamp)
                else: 
                    stamps.append(0)
        i += 1    
    return (words,stamps)

#TODO: returns a file with a flattened lemmatized transcript
def lemmetize_files(file_array):
    return 0

def lemmetize_transcript(str):
    return 0

def remove_time_stamps(str):
    return 0


# lemmatizes and removes time stamps 

def generate_flattened_transcript(path):
    
    
    return transcript_str

#HELPER
def mutual_information(other, co_occurrences, absolute_occurrences, target):
    return co_occurrences[other] / (absolute_occurrences[target] * absolute_occurrences[other])



#pick a target word and count the number of times each word appears "close to" the target word
#minimum lexicon size is 30
#generates a lexicon from a flattened, lemmatized file.
#takes as input n_words, the desired number of words in the output lexicon
def lexicon_from_flattened_files(filename, target, n_words):
    window = 10  #number of words to be examined at any one time in a window

    words = []
    if(n_words < 30): n_words = 30
    
    file = open(filename, "r")
    for line in file:
        for word in line.split(' '):
            words.append(word)

    absolute_occurrences = defaultdict(int)

    for word in words:
        absolute_occurrences[word] += 1
      
    pairs = [(k, v) for k, v in absolute_occurrences.items()]
    sorted_pairs = sorted(pairs, key = itemgetter(1), reverse=True)
    co_occurrences = defaultdict(int)

    for i in list(range(window, len(words) - window)):
        if words[i] == target:
            for j in range(i - window, i + window):
                co_occurrences[words[j]] += 1

    pairs = [(k, v) for k, v in co_occurrences.items()]
    sorted(pairs, key=itemgetter(1), reverse=True)

    mi_pairs = [(word, mutual_information(word, co_occurrences, absolute_occurrences, target)) for word in set(words)]
    mi_pairs_filtered = [pair for pair in mi_pairs if absolute_occurrences[pair[0]] > 100]
    mi_pairs_sorted = sorted(mi_pairs_filtered, key=itemgetter(1), reverse=True)
    
    topic_words = [ mi_pairs_sorted[i][0] for i in range(0,n_words)]

    return topic_words


#takes a string in format (time1s --> time1e, time2s --> time2e) 
#and returns either time1s(the overall start time) or time2e(the overall end time) based on passed in parameter
def isolateTimeSegment(part, timeRange):
    
    start_time = ''
    end_time =''
    ignoreChar1 = '>'
    ignoreChar2 = ' '
    ignoreChar3 = '-'
    end = 0
    
    if (part == 1):
        tRange = timeRange[0]
    else:
        tRange = timeRange[1]
        
    for char in tRange:
        #print(char)
        if char == '-':
            end = 1
            #print('begin end')
        if(char != ignoreChar1 and char != ignoreChar2 and  char != ignoreChar3):
            if(end == 0):
                start_time = start_time + char
            else:
                end_time = end_time + char
            #print(start_time, end_time)
                
    if part == 1:
        return start_time
    else:
        return end_time

# returns an array that holds the segments about the topic. In  entry i in th array
# arr[0] is the string ar[1] is the immigration score, ar[2] is the sentiment scores
# arr[3] is the start and end of the window


# var suggestions
# window_size = 100
# skip = 70
# score_threshold = 110

def combine_overlapping_intervals(scores_filtered, times_raw):
    topic_indexes_and_times = []

    i = 1

    while i < len(scores_filtered): 
        current_score_intvl = scores_filtered[i]
        previous_score_intvl = scores_filtered[i-1]
        start = scores_filtered[i-1][0]

        #determine if ranges of the two scores overlap
        if current_score_intvl[0] <= previous_score_intvl[1]: #if the beginning of the current interval overlaps with the end of the interval before
            expanded_end = scores_filtered[i][1]

            scores_filtered.insert(i, ((start, expanded_end))) #
            scores_filtered.remove(current_score_intvl)
            scores_filtered.remove(previous_score_intvl)
            #new_times.append((start_time, expanded_end_time))
            
        else: 
            i = i + 1
        #new_times.append((start_time, end_time))
    #print(scores_filtered[i])
    #print(times_raw[scores_filtered[i][0]])

    #holds the start and beginning indexes of words in expanded topic segments, and their corresponding times
    
    for x in range(0, len(scores_filtered)):
        elemIndexes = scores_filtered[x] #format: (strtInd, endInd)
        startRange = times_raw[elemIndexes[0]]
        endRange =  times_raw[elemIndexes[1]]
        topic_indexes_and_times.append((elemIndexes, (startRange, endRange)))

    return topic_indexes_and_times


def print_topic_segments(string_score_sent):
    for entry in string_score_sent:
        print('hi')
        print(entry[0])
        print("topic score: ", entry[1])
        print("sentiment score: ", entry[2])

def write_topic_segments_in_file(string_score_sent, filename):
    for entry in string_score_sent:
        file = open(filename, "w")
        file.write(entry[0])
        file.write("topic score : ", entry[1])
        file.write("sentiment score: ", entry[2])
  
#HELPER

# scores_filtered = combine_overlapping_intervals(scores_filtered, segments, times)
#assumes lexicon greater than 30
#TODO: make score based upon size of lexicon window maybe... / edit
def compute_topic_score(string, topic_words):
    #nlp = spacy.load('en_core_web_sm', disable=['parser','ner'])
    #print('len(topic_words)', len(topic_words))
    score = 0
    for word in string.split(' '):
        #doc = nlp(word)
        #for token in doc:
            #word = token.lemma_

        #print('word: ', word)
        #if word == 'immigration': print('word: ', word)

        ##work around... fix later....
        #for lex_word in topic_words:
            #if(lex_word in word):
                #word = lex_word

       # if (lex_word in word for lex_word in topic_words):
        if word in topic_words:
            #print('***word is in topic words:', word)
            topic_rank = topic_words.index(word)
            if (topic_rank ==0): score += 100 # main topic word always scored at index 0
            if (topic_rank in range (1, 10)): score += 20
            if (topic_rank in range (10, 20)): score += 15
            if (topic_rank in range (20, 30)): score += 10
            if (topic_rank in range (30, len(topic_words) - 1)): score += 7
    #print('topic score: ', score)
    return score

#takes in an array of size window_size and computes a score
#takes in an array of size window_size and computes a score
def compute_sent_score(string):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = 0
    for word in string.split(' '):
        sentiment_score += analyzer.polarity_scores(word)['compound']
    return sentiment_score


#returns an array of segments and the times and indexes in the word array 
# they correspond to.

#if you comment out lines that have # next to 
#it you will get non overlapping segements
#
def create_segments(filename, path, overlap, segment_length, skip):
    ar = parse_file(filename, path)
    words = ar[0]
    stamps = ar[1]
    segments = []
    times = []
    indexes = []
    
    #****** lemmatized_segments = []
    
    #beginning_index=0
    last_index = 0 #the last index of the last segment that has been apended. 
    end = len(words)

    while(last_index + segment_length < end):
        #print('looping again', last_index, segment_length, len(words))
        beginning_index = last_index
        last_index += segment_length
        dot_index = non_zero_index(stamps[last_index:])
        last_index += dot_index
        
        #if (last_index + dot_index > end):
            #words = words[:last_index + dot_index]
            #ar2 = [segments, times, indexes, words, stamps]
            #return ar2
        #if(last_index == end) last_index = last_index - 1 #take out
        
        #print('beginning_index:', beginning_index, 'last_index: ', last_index, len(stamps) )
        
        if (last_index >= end): #account for case in which file doesn't end with a period
            last_index = end - 1
            #print('ignoring last segment', last_index) #fix: actually ignore last segment
            break

        new_segment = ' '.join(words[beginning_index + 1 :last_index + 1])
        segments.append(new_segment)

        #***** lemmatized_segments_text.append(lemmatize_segment(new_segment))
            #GEN: text then compute the topic score on lemmatized segment and store

        times.append((stamps[beginning_index], stamps[last_index]))
        indexes.append((beginning_index,last_index))
        if (overlap == 'overlap'):
            dot_skip = non_zero_index(stamps[beginning_index + skip:])##
            last_index = beginning_index + skip + dot_skip ###

    ar2 = [segments, times, indexes, words, stamps]

    return ar2

#returns an array of words with high enough scores. Also returns the start and end indexes of the words
#format: ((strtInd, endInd), segmentScore)
def get_filtered_scores(segments, lexicon, indexes, score_threshold):
    i = 0
    scores = [] #holds scores

    for segment in segments:

        #score section
        score = compute_topic_score(segment, lexicon) 

        #add the score 
        scores.append(((indexes[i]), score))

        i = i + 1

    #store indexes of the intervals of words with high enough scores: i: ((strtInd, endInd), segScore)
    scores_filtered = [interval for (interval, score) in scores if score > score_threshold] #took out times_raw
    print('len(scores_filtered): ', len(scores_filtered))
    return scores_filtered

def foobar():
    pass

#returns an array of transcript segments about a given topic and corresponding information:
#array[i][0]: the transcript segment
#array[i][1]: the segment's topic score
#array[i][2]: the segment's sentiment score
#array[i][3]: the segment's start time
#array[i][3]: the segment's end time

def identify_segments_about(file, path, overlap, segment_length, skip, lexicon, score_threshold):
    
    ar = create_segments(file, path, overlap, segment_length, skip)
    
    segments = ar[0]
    times = ar[1]
    indexes = ar[2] #stores word indexes of a segment i
    words = ar[3]
    times_raw = ar[4]
    
    scores_filtered = list(get_filtered_scores(segments, lexicon, indexes, score_threshold))
    print('len(scores_filtered): ', len(scores_filtered))
    topic_indexes_and_times = combine_overlapping_intervals(scores_filtered, times_raw)
    #scores_times = lib.combine_overlapping_intervals(scores_filtered, times_raw)
    
    string_score_sent_timestamp = []
    Record = namedtuple('Point', ['text', 'topic_score', 'sent_score', 'start_time', 'end_time', 'file'])


    for i in range(0, len(topic_indexes_and_times)): #
        new_segment = []
        seg_start = topic_indexes_and_times[i][0][0] + 1
        seg_end = topic_indexes_and_times[i][0][1] + 1
        string = ' '.join(words[seg_start : seg_end])

        #find topic and sentiment scores -- topic score is already stored somewhere... fix
        topic_score = compute_topic_score(string, lexicon)
        sentiment_score = compute_sent_score(string)

        #find time ranges
        timeRange = topic_indexes_and_times[i][1]
        start_time = isolateTimeSegment(1, timeRange)
        end_time = isolateTimeSegment(2, timeRange)


        #new_entry = ((string, score, sentiment_score, start_time, end_time, file))
        new_segment = Record(text=string, topic_score=topic_score, sent_score=sentiment_score, start_time=start_time,end_time=end_time,file=file)



        string_score_sent_timestamp.append(new_segment)
        
    return string_score_sent_timestamp
