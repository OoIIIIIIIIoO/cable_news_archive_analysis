
# coding: utf-8

# In[1]:


from collections import defaultdict 
import pysrt 
import os
from tqdm import tqdm

import spacy


# In[4]:


#load database files from computer

path='/Users/theodoraboulouta/Desktop/CS206/subs'
all_subtitles = os.listdir(path)
all_subtitles


# In[5]:


#show first file loaded

file = all_subtitles[0]
file


# In[6]:


#show starting text of first file

print(open(path + '/' + file).read())


# In[7]:


#make every file flat and add to the list

full_flat_transcript = [] #contains a list with a flat transcript of each document


for a_file in tqdm(all_subtitles):
    #pick next file in the folder
    srt_file = pysrt.open(path + '/' + a_file)
    flat_transcript = ''
    
    #make flat
    for item in srt_file:
        flat_transcript += item.text + ' '
    full_flat_transcript.append(flat_transcript)


# In[7]:


#show flattened version of first file 

print('total number of files: ', len(full_flat_transcript))

index = 0;
print ('flattened file #', index + 1, ': \n')
print(full_flat_transcript[index])


# In[14]:



# create a lemmatized version of each individual file and store this back in the original full_flat_transcript position  

nlp = spacy.load('en_core_web_sm', disable=['parser','ner'])

i = 0

max_index = len(full_flat_transcript) - 1 
print(max_index)

#demo of first file lemmatized
for t_file in nlp.pipe(tqdm(full_flat_transcript), n_threads = 4, batch_size = 100): #reduce batch size if load is too much
    lem_flat_transcript = ''
    
    for token in t_file: #iterate through and lemmatize each word in the file
        lem_flat_transcript += token.lemma_ + ' '
 
    #replace old flat transcript with new, lemmatized flat transcript
    full_flat_transcript[i] = lem_flat_transcript
    i += 1   #move to the next transcript file in the list
    
#remove punctuation
#lem_flat_transcript = lem_flat_transcript.translate(None, string.punctuation)
    
#maybe store something here about start index of certain channels, then start character ranges, for later transcript parsing


# In[15]:


#show new, lemmatized flat transcript, stored in original list

print(full_flat_transcript[0])


# In[16]:


#combine flat transcripts across lemmatized files
combined_flat_lem_transcript = ''


for word in full_flat_transcript:
    combined_flat_lem_transcript += word + ' '  


# In[17]:


#combined transcript now contains words from the first 100 files

print(combined_flat_lem_transcript[:1000])


# In[18]:


#make a list of all the words (these will all be already lemmatized at this point)

words = combined_flat_lem_transcript.split(' ')
#double_words = [] # code for n-grams

print(words[:100])


# In[2]:


#count the number of occurences of each word

absolute_occurrences = defaultdict(int)

for word in tqdm(words):
    absolute_occurrences[word] += 1


# In[3]:


#show number of occurences of each word

from operator import itemgetter
pairs = [(k, v) for k, v in absolute_occurrences.items()]
sorted_pairs = sorted(pairs, key=itemgetter(1), reverse=True)
sorted_pairs


# In[1]:


#pick a target word and count the number of times each word appears "close to" the target word

target = "crime"

co_occurrences = defaultdict(int)
window = 10

for i in tqdm(list(range(window, len(words) - window))):
    if words[i] == target:
        for j in range(i - window, i + window):
            co_occurrences[words[j]] += 1
            


# In[20]:


#show co-occurence counts

from operator import itemgetter
pairs = [(k, v) for k, v in co_occurrences.items()]
sorted(pairs, key=itemgetter(1), reverse=True)


# In[25]:


def mutual_information(other):
    return co_occurrences[other] / (absolute_occurrences[target] * absolute_occurrences[other])


# In[26]:


mi_pairs = [(word, mutual_information(word)) for word in tqdm(set(words))]


# In[30]:


mi_pairs_filtered = [pair for pair in mi_pairs if absolute_occurrences[pair[0]] > 100]
mi_pairs_sorted = sorted(mi_pairs_filtered, key=itemgetter(1), reverse=True)
mi_pairs_sorted[0][0]
mi_pairs_sorted


# In[38]:


#put lexicon into array in order of strongest to weakest match
topic_words = [ mi_pairs_sorted[i][0] for i in range(0,200)]

topic_words


# In[149]:


combined_flat_lem_transcript[:1000]


# In[391]:


#topic identification


#create an array list of all the words in the files in order: to be used to score sections
i = 1
lemmas = [] #holds the words in the files in order

file = open("test_fox", "r")

for line in file:
    for word in line.split(' '):
        lemmas.append(word)
        i+= 1
    


# In[392]:


#score sections
   
window_size = 100 #2 minute chunks
skip = 70 #analyze with an accuracy of 30 seconds, 30 seconds = 70 words

scores = [] #holds scores

#topic_words: an array of words from the lexicon, ordered by MI score
#with index 0 being the topic word and lower indexes containing words with higher MI scores (generated and manual)
#threshhold_score = 5

#takes in an array of size window_size and computes a score
topic_words = ['immigration','comprehensive','stance','reform','illegal','soften','lawful','postpone','cornerstone','flopping','phoenix','compliance','flop','custom','suspend','enforce','hawk','temporarily','softening','pillar','systematically','centerpiece','entitlement','fiery','skilled','restrict','outline','speech','statu','signature','liner','waiver','amnesty','policy','hardening','appealing','federation','harden','realistically','revise','proposal','denigrate','sensible','adequate','ambiguity','i.c.e','input','disproportionately','forefront','backtrack','univision','reversal','sovereignty','downward','tirade','nationalism','clarify','position','trade','curb','nuanc','influx','deportation','anticipate','flip','mixed','deter','migration','screening','citizenship','arizona','revert','border','detention','terminate','legislative','trafficking','wednesday','clarity','tweak','vetting','coulter','nonwhite','belgium','undocumented','visa','staunch','sanctuary','pertain','topic','professionally','unveil','meaningful','refugee','clarification','akron','vaughn','misrepresent','latinos','removal','evolve','shift','modeling','articulate','loudly','proponent','thereof','harsh','mantra','upward','coherent','deport','cliche','arpaio','tackle','germany','enrique','slick','jeb','renegotiate','monte','laughable','pathway','compassionate','cantor','humane','hatred','conservatism','heritage','remarkably','civilization','radically','prioritize','vet','polici','alien','landmark','merkel','modest','mechanism','major','crop','specificity','strict','wage','wrestle','mexico','confusing','bigotry','broken','await','enforcement','immigrant','deliver','documentation','volatile','signal','properly','principle','mobility','legal','cortez','establish','entry','feasible','hallmark','mercy','listener','accelerate','issue','anti','historical','consideration','blowback','overhaul','ethnic','rhetoric','mack','humanely','trumpism','reaffirm','aspirational','propose','waver','me','detailed','construction','ban','plan','compromise','clueless','hindsight','soft','reconcile','sharia','pace','seemingly','manpower','thursday','impulse']

def compute_topic_score(window):
   score = 0
   for word in window:
       if word in topic_words:
           topic_rank = topic_words.index(word)
           if (topic_rank ==0): score += 100 # main topic word always scored at index 0
           if (topic_rank in range (1, 10)): score += 20
           if (topic_rank in range (10, 20)): score += 15
           if (topic_rank in range (20, 30)): score += 10
           if (topic_rank in range (30, len(topic_words) - 1)): score += 7
   return score


# In[393]:


#topic ID
skip = 70
#iterate through lemmas list for a single transcript, skipping from i =0 to i = 70, for example
for i in range(0, len(lemmas), skip):
    window = lemmas[i:i+window_size] #get an array of size 280
    string =''
    for word in window:
        string += word + ' '
    print(string)
    
    score = compute_topic_score(window)
    print('score', score, '\n ------- \n')
    scores.append(((i, i+window_size), score))


# In[394]:


scores[:100]


# In[395]:


from matplotlib import pyplot as plt


# In[396]:


#show graph of various intvl scores

X = [intvl[0] for (intvl, score) in scores]
Y = [score for (intvl, score) in scores]
plt.plot(X, Y) 

#plot of topic match by starting time interval


# In[397]:


score_threshold = 110 #can pick this based on a plot of the scores

#make scores contain only a list of intervals with high enough topic-match scores

scores_filtered = [interval for (interval, score) in scores if score > score_threshold]


# In[398]:


scores_filtered = list(scores_filtered)
print(scores_filtered)


# In[399]:


#visualization: length of "topic" segments (pre-merge)

X = [intvl[0] for intvl in scores_filtered]
Y = [(intvl[1]-intvl[0]) for intvl in scores_filtered]
plt.plot(X, Y) 


#X = [intvl[0] for (intvl, score) in scores]
#Y = [score for (intvl, score) in scores]
#plt.plot(X, Y) 

#plot of topic match by starting time interval


# In[400]:


#combine overlapping intervals: new interval stored in scores is expanded


i = 1
print(i)

while (i < len(scores_filtered)): 
    print('i = ', i)
    print('len scores' , len(scores_filtered))
    
    current_score_intvl = scores_filtered[i]
    previous_score_intvl = scores_filtered[i-1]
    start = scores_filtered[i-1][0]
    
    print('previous intvl:', previous_score_intvl, 'index:' , i-1)
    print('current intvl:', current_score_intvl, 'index:' , i)
   
    #determine if ranges of the two scores overlap
    if (current_score_intvl[0] <= previous_score_intvl[1]): #if the beginning of the current interval overlaps with the end of the interval before
        #print('merging. pre-merge:')
        
        #print( scores_filtered[i-2], scores_filtered[i-1], scores_filtered[i], '(I)', scores_filtered[i+ 1])
        #combine scores
        #previous_score_intvl[1] = current_score_intvl[1] #extend index of previous score to be the last index of the current score
 
        expanded_end = scores_filtered[i][1]

        #print('intvl at index i-1 (= ', (i-1), '):  ', scores_filtered[i-1], ' (previous)' )
        #print('intvl at index i (= ', i, '): ',  scores_filtered[i], ' (current)' , i)
        
        scores_filtered.insert(i, (start, expanded_end))
            
        #remove current score once joined
        scores_filtered.remove(current_score_intvl)
        scores_filtered.remove(previous_score_intvl)
        
       
        #scores_filtered[i-1][1] = expanded_end
        
        #del scores_filtered[i]
        #print('post-merge:')
        #print(scores_filtered[i-2], scores_filtered[i-1], scores_filtered[i], '(I)', scores_filtered[i+ 1])
               
        #print('intvl at index i-1 (= ', i-1, '): ', scores_filtered[i-1], ' (previous)' )
        #print('intvl at index i (= ', i, '): ', scores_filtered[i], ' (current)')
        #print('i = ', i)

    else: 
        #print(' not merging' )
        #move to next index if no joining occured
        i += 1

scores_filtered
print(len(scores_filtered))

#for i in range(1, len(scores):


# In[401]:


#visualization: length of "topic" segments (post-merge)

X = [intvl[0] for intvl in scores_filtered]
Y = [(intvl[1]-intvl[0]) for intvl in scores_filtered]
plt.plot(X, Y) 


# In[402]:


#sentiment analysis of a string 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()


#takes in an array of size window_size and computes a score
def compute_sent_score(string):
    sentiment_score = 0
    
   
    #strings
    sentiment_array = [string, ]
    #sentiment_array[0] = string
    
    for word in sentiment_array:
        sentiment_score += analyzer.polarity_scores(word)['compound']
        
    return sentiment_score


# In[403]:


#score = compute_sent_score('hey how are you doing babe i hate you and love you at the same time')
#print(score)
print(len(scores_filtered))


# In[404]:


#print out identified topic sections
    #iterate through scores
    #print from lemma from interval[0] to interval[1]

string_score_sent = []

#iterate through lemmas list for a single transcript, skipping from i =0 to i = 70, for example
print(len(scores_filtered))
for i in range(0, len(scores_filtered)):
    window_start = scores_filtered[i][0]
    window_end = scores_filtered[i][1]
    window = lemmas[window_start:window_end] #get an array of size 280
    string =''
    for word in window:
        string += word + ' '
    print(string)
    
    score = compute_topic_score(window)
    print('Section score:', score)
    
    sentiment_score = compute_sent_score(string)
    print('Sentiment score:', sentiment_score, '\n ------- \n')
    
    string_score_sent.append((string, score, sentiment_score, (window_start, window_end)))
   


# In[405]:


#sentiment analysis: how positive are these topic
    
string_score_sent[:3]


# In[406]:


#visualization: #visualization: sentiment scores for each segment(post-merge)


#string_score_sent.append((string, score, sentiment_score, (window_start, window_end)))

X = [item[3][0] for item in string_score_sent]
Y = [item[2] for item in string_score_sent]
plt.plot(X, Y)

