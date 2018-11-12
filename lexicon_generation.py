
# coding: utf-8

# In[79]:


from collections import defaultdict 
import pysrt 
import os
from tqdm import tqdm
import spacy
from operator import itemgetter


# In[80]:


def mutual_information(other, co_occurrences, absolute_occurrences, target):
    return co_occurrences[other] / (absolute_occurrences[target] * absolute_occurrences[other])


# In[81]:


#pick a target word and count the number of times each word appears "close to" the target word
def generate_lexicon(filename, target, n_words):
    words = []
    
    file = open(filename, "r")
    for line in file:
        for word in line.split(' '):
            words.append(word)

   # target = "immigration"
    absolute_occurrences = defaultdict(int)

    for word in tqdm(words):
        absolute_occurrences[word] += 1
      
    pairs = [(k, v) for k, v in absolute_occurrences.items()]
    sorted_pairs = sorted(pairs, key=itemgetter(1), reverse=True)
    sorted_pairs

    co_occurrences = defaultdict(int)
    window = 10

    for i in tqdm(list(range(window, len(words) - window))):
        if words[i] == target:
            for j in range(i - window, i + window):
                co_occurrences[words[j]] += 1

    pairs = [(k, v) for k, v in co_occurrences.items()]
    sorted(pairs, key=itemgetter(1), reverse=True)

    mi_pairs = [(word, mutual_information(word, co_occurrences, absolute_occurrences, target)) for word in tqdm(set(words))]
    mi_pairs_filtered = [pair for pair in mi_pairs if absolute_occurrences[pair[0]] > 100]
    mi_pairs_sorted = sorted(mi_pairs_filtered, key=itemgetter(1), reverse=True)
    mi_pairs_sorted[0][0]
    mi_pairs_sorted
    
    topic_words = [ mi_pairs_sorted[i][0] for i in range(0,n_words)]

    return topic_words


# In[82]:


fox_lexicon = generate_lexicon("fox","sexual", 1000)
msnbc_lexicon = generate_lexicon("msnbc","sexual", 1000)
cnn_lexicon = generate_lexicon("cnn","sexual", 1000)
fox_lexicon
msnbc_lexicon
cnn_lexicon


# In[83]:


#WORDS ONLY IN FOX

for word in fox_lexicon[:50]:
    if word not in cnn_lexicon:
        if word not in msnbc_lexicon:
            print(word)


# In[84]:


#WORDS IN CNN

for word in cnn_lexicon[:50]:
    if word not in fox_lexicon:
        if word not in msnbc_lexicon:
            print(word)


# In[85]:


#WORDS IN MSNBC

for word in msnbc_lexicon[:50]:
    if word not in fox_lexicon:
        if word not in cnn_lexicon:
            print(word)

