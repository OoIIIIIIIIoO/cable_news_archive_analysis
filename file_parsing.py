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

#the functions in this file handle file parising
# specific to the format the inetrenet archive transcripts are in

#takes in a list of words and capitalized it
def capitalizeLexicon(lexicon):

    cap_lexicon = []
    for word in lexicon:
        word = word.upper()
        cap_lexicon.append(word)
    return cap_lexicon

#finds the first non zero index of an array
def non_zero_index(ar):
    i = 0
    while ( i < len(ar) and ar[i] == 0 ):
        i+=1
    return i

#returns the date of a segment
def get_Date(segment):
    string = segment.file
    ar = ''
    ar = string.split('_')
    s = ar[1]
    #k = ar[2]
    date = s[0:4] + '_' + s[4:6] + '_' + s[6:8] #+ '_' + k
    return date

# parsed in the file into sentences and keeps track of its corresponding time stamp in the cable news transcript.
def parse_file(filename, path):
    file = open(path + '/' + filename, "r", encoding="ISO-8859-1")
    words = []
    stamps = []
    timestamp = 0
    i = 0   
    for line in file:
        line = line.strip()       
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

#given a string of the time range the function returns the strat time and end time 
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
        if char == '-':
            end = 1
        if(char != ignoreChar1 and char != ignoreChar2 and  char != ignoreChar3):
            if(end == 0):
                start_time = start_time + char
            else:
                end_time = end_time + char                
    if part == 1:
        return start_time
    else:
        return end_time


def write_topic_segments_in_file(string_score_sent, filename):
    for entry in string_score_sent:
        file = open(filename, "w")
        file.write(entry[0])
        file.write("topic score : ", entry[1])
        file.write("sentiment score: ", entry[2])

#creates segments of full sentences given a filename. The segments have a rough length of segment_length
def create_segments_transcripts(filename, path, overlap, segment_length, skip):
    ar = parse_file(filename, path)
    words = ar[0]
    stamps = ar[1]
    segments = []
    times = []
    indexes = []
    last_index = 0 #the last index of the last segment that has been apended. 
    end = len(words)

    while(last_index + segment_length < end):
        beginning_index = last_index
        last_index += segment_length
        dot_index = non_zero_index(stamps[last_index:])
        last_index += dot_index
        
        if (last_index >= end): #account for case in which file doesn't end with a period
            last_index = end - 1
            break

        new_segment = ' '.join(words[beginning_index + 1 :last_index + 1])
        segments.append(new_segment)

        times.append((stamps[beginning_index], stamps[last_index]))
        indexes.append((beginning_index,last_index))
        if (overlap == 'overlap'):
            dot_skip = non_zero_index(stamps[beginning_index + skip:])##
            last_index = beginning_index + skip + dot_skip ###

    ar2 = [segments, times, indexes, words, stamps]

    return ar2

def create_segments_text(filename, overlap, segment_length, skip): #WORKS
    words = read_words_in_file_articles(filename)
    segments = []
    indexes = []

    last_index = 0 #the last index of the last segment that has been apended. 
    end = len(words)
    dot_index = 0 #words.index('.')
    i = 0
    while(last_index + segment_length < end):

        beginning_index = last_index + 1
        last_index += segment_length

        if ((last_index >= end) or ('.' not in words[last_index:])): #account for case in which file doesn't end with a period
            last_index = end - 1
            break

        dot_index = words[last_index:].index('.')
        last_index += dot_index
        new_segment = ' '.join(words[beginning_index + 1 :last_index + 1])
        segments.append(new_segment) # new segmnets are correct, is indexing correct?

        # print('NEW SEGMENT: ', new_segment)
        # print('FIRST WORD', words[beginning_index], 'LAST WORD' ,words[last_index], 'LAST INDEX', last_index)
        # print('\n')
        indexes.append((beginning_index,last_index))
        if (overlap == 'overlap'):
            dot_skip = words[beginning_index + skip:].index('.')
            last_index = beginning_index + skip + dot_skip
    ar2 = [segments, indexes, words]

    return ar2

def dateScore(dateStr):
    valStr =  dateStr[0:4] + dateStr[5:7] + dateStr[8:10]
    return (int(valStr))

#returns an array fo all the words in a file
def read_words_in_file(filename):
    words = []
    file = open(filename, "r")
    for line in file:
        for word in line.split(' '):
            words.append(word)
    file.close()
    return words

def read_words_in_file_articles(filename):
    words = []
    file = open(filename, "r")
    for line in file:
        line = line.replace('.', ' . ')
        for word in line.split(' '):
            if not word == ' ':
                words.append(word)
    file.close()
    return words
