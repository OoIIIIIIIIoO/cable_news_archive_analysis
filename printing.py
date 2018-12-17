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

# this file handles printing functions 

def printSegment(segment, label):
    print(label, segment.text, '\n')
    print('Topic score: ', segment.topic_score, ',', 'Sentiment score: ', segment.sent_score, 'Bias score: ', segment.bias_score)
    print('Time range: ', segment.start_time, ' - ', segment.end_time)
    print('Original File: ', segment.file, '\n') 
    print('------------------ \n')

def printTopicSegments(all_segments, n_segments):
    i = 0
    for segment in all_segments[:n_segments]:
        label = str(i) + ':'
        printSegment(segment, label)
        i+=1

def print_topic_segments(string_score_sent):
    for entry in string_score_sent:
        print(entry[0])
        print("topic score: ", entry[1])
        print("sentiment score: ", entry[2])

def printPeaks(axes, num_vals, max):
    
    x = axes[0]
    y= axes[1]

    frequencies = [(x[i],y[i]) for i in range(0,len(x))]
    sorted_freqs = sorted(frequencies, key=itemgetter(1))
    reverse_sorted_freqs = sorted(frequencies, key=itemgetter(1), reverse=True)
    if max:
        for i in range(0,num_vals):
            print(reverse_sorted_freqs[i][0], ': ', reverse_sorted_freqs[i][1])
    else:
        for i in range(0,num_vals):
            print(sorted_freqs[i][0], ': ', sorted_freqs[i][1])

def printSegmentsFromDate(dateStr, segments):
    i =0
    index = 0
    
    for segment in segments:
        file_name = segment.file
        
        if(dateStr in segment.file):
            stringNum= str(i) + ':'
            print('index:', index)
            printSegment(segment, stringNum)
            i+=1
        index += 1