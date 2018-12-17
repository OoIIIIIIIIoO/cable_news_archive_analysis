from collections import defaultdict 
import pysrt 
from tqdm import tqdm
import spacy
from operator import itemgetter
import re
from collections import namedtuple
from collections import defaultdict 
import pysrt 
import os
from tqdm import tqdm
import spacy
import re
from collections import namedtuple
from operator import itemgetter

import modules_comp_journ as lib
import file_parsing as files

#returns the mutual-information index given the co-occurances and absolute occurances
def mutual_information(other, co_occurrences, target, absolute_occurrences):
    return co_occurrences[other] / (absolute_occurrences[target] * absolute_occurrences[other])

#keeps track of the number of cooccurences of the words in the wile with our target word
def get_co_occurrences(words, target, window):
    co_occurrences = defaultdict(int)
    window = 10

    for i in tqdm(list(range(window, len(words) - window))):
        if words[i] == target:
            for j in range(i - window, i + window):
                co_occurrences[words[j]] += 1
                
    return co_occurrences

#keeps track of the absolute occurences of words
def get_absolute_occurrences(words):
    absolute_occurrences = defaultdict(int)
    for word in tqdm(words):
        absolute_occurrences[word] += 1
    
    return absolute_occurrences

#return a lexicon related to the 'target' word based on the filename. The lexicon contains n_words
def generate_lexicon(filename, target, n_words):
    window = 10
    words = files.read_words_in_file(filename)
    if target not in words:
        print('topic word not in text')
    
    absolute_occurrences = get_absolute_occurrences(words)
    co_occurrences = get_co_occurrences(words, target, window)
    pairs = [(k, v) for k, v in absolute_occurrences.items()]
    sorted(pairs, key=itemgetter(1), reverse=True)

    pairs = [(k, v) for k, v in co_occurrences.items()]
    sorted(pairs, key=itemgetter(1), reverse=True)

    mi_pairs = [(word, mutual_information(word, co_occurrences, target, absolute_occurrences)) for word in tqdm(set(words))]
    mi_pairs_filtered = [pair for pair in mi_pairs if absolute_occurrences[pair[0]] > 100]
    mi_pairs_sorted = sorted(mi_pairs_filtered, key=itemgetter(1), reverse=True)    
    topic_words = [ mi_pairs_sorted[i][0] for i in range(0,n_words)]
    return topic_words