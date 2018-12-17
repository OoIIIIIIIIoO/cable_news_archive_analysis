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
import file_parsing as files



# combines adjecent segmnets that are about a specific topic,for news transcripts
def combine_overlapping_intervals_transcripts(scores_filtered, times_raw):
    topic_indexes_and_times = []

    i = 1

    while i < len(scores_filtered): 
        current_score_intvl = scores_filtered[i]
        previous_score_intvl = scores_filtered[i-1]
        start = scores_filtered[i-1][0]

        if current_score_intvl[0] <= previous_score_intvl[1]: 
            expanded_end = scores_filtered[i][1]

            scores_filtered.insert(i, ((start, expanded_end))) 
            scores_filtered.remove(current_score_intvl)
            scores_filtered.remove(previous_score_intvl)
            
        else: 
            i = i + 1
    
    for x in range(0, len(scores_filtered)):
        elemIndexes = scores_filtered[x] 
        startRange = times_raw[elemIndexes[0]]
        endRange =  times_raw[elemIndexes[1]]
        topic_indexes_and_times.append((elemIndexes, (startRange, endRange)))

    return topic_indexes_and_times


# combines adjecent segmnets that are about a specific topic. 
def combine_overlapping_intervals_text(scores_filtered):
    topic_indexes_and_times = []

    i = 1
    while i < len(scores_filtered): 
        current_score_intvl = scores_filtered[i]
        previous_score_intvl = scores_filtered[i-1]
        start = scores_filtered[i-1][0]

        if current_score_intvl[0] <= previous_score_intvl[1]: 
            expanded_end = scores_filtered[i][1]

            scores_filtered.insert(i, ((start, expanded_end))) 
            scores_filtered.remove(current_score_intvl)
            scores_filtered.remove(previous_score_intvl)      
        else: 
            i = i + 1
    
    for x in range(0, len(scores_filtered)):
        elemIndexes = scores_filtered[x] 
        topic_indexes_and_times.append(elemIndexes)

    return topic_indexes_and_times

#returns the combined scores
def getSentScoreArrays(segments):
    
    scores = [(files.get_Date(seg), seg.sent_score) for seg in segments]
    sorted_scores = sorted(scores, key=itemgetter(0))

    score_dict = {} #stores scores by rate

    for (date, score) in sorted_scores:
        if date in score_dict:
            score_dict[date] = score_dict[date] + score
        else:
            score_dict[date] = score   
    
    X = [date for (date, score) in score_dict.items()]
    Y = [score for (date, score) in score_dict.items()]

    return [X,Y]

#returns the combined scores
def getBiasScoreArrays(segments):
    
    scores = [(files.get_Date(seg), seg.bias_score) for seg in segments]
    sorted_scores = sorted(scores, key=itemgetter(0))

    score_dict = {} #stores scores by rate

    for (date, score) in sorted_scores:
        if date in score_dict:
            score_dict[date] = score_dict[date] + score
        else:
            score_dict[date] = score   
        
    
    X = [date for (date, score) in score_dict.items()]
    Y = [score for (date, score) in score_dict.items()]

    return [X,Y]

#returns the frequency of mentions
def getFrequencyArrays(segments):
    
    scores = [(files.get_Date(seg), seg.topic_score) for seg in segments]
    sorted_scores = sorted(scores, key=itemgetter(0))

    score_dict = {} 

    for (date, score) in sorted_scores:
        if date in score_dict:
            score_dict[date] = score_dict[date] + 1
        else:
            score_dict[date] = 1   
    
    X = [date for (date, score) in score_dict.items()]
    Y = [score for (date, score) in score_dict.items()]

    return [X,Y]
    
