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
import modules_comp_journ as lib


#plots sentiment scores 
def plotSentScores(segments, labelStr):
    
    axes = lib.getSentScoreArrays(segments) #HERE
    x = axes[0]
    y= axes[1]
    plt.rcParams['figure.figsize'] = [10*1.5, 4*1.5] ##
    
    fig=plt.figure()    
    ax=fig.add_subplot(111)
    plt.xlabel('date')
    plt.ylabel('Aggregate sentiment scores')
    title = 'Aggregate sentiment scores by date: ' + labelStr
    plt.title(title, fontsize=16, fontweight='bold')
    plt.plot(x,y, label=labelStr)
    plt.legend(loc='upper right')    
    ax.xaxis.set_major_locator(plt.MaxNLocator(9)) ##
    ax.axhline(y=0, xmin=0, xmax=1, linestyle='--', color='grey')
     
    filename = labelStr + '_score_plot.png'
    fig.savefig(filename)

#plots bias scores
def plotBiasScores(segments, labelStr):
    
    axes = lib.getBiasScoreArrays(segments) #HERE
    x = axes[0]
    y= axes[1]
    plt.rcParams['figure.figsize'] = [10*1.5, 5*1.5] ##
    
    fig=plt.figure()
    
    ax=fig.add_subplot(111)
    
    plt.xlabel('date')
    plt.ylabel('aggregate bias score')
    title = 'Politically-biased language use: ' + labelStr 
    plt.title(title, fontsize=16, fontweight='bold')

    plt.plot(x,y, label=labelStr)
    plt.legend(loc='upper right')
    
    ax.xaxis.set_major_locator(plt.MaxNLocator(9))
    ax.axhline(y=0, xmin=0, xmax=1, linestyle='--', color='black')
    
    filename = labelStr + '_score_plot.png'
    fig.savefig(filename)

#plots frequency of topic mentions
def plotFrequency(segments, labelStr):
    
    axes = lib.getFrequencyArrays(segments)  #HERE
    x = axes[0]
    y= axes[1]
    plt.rcParams['figure.figsize'] = [15, 10] ##
    
    
    fig=plt.figure() 
    ax=fig.add_subplot(2,1,1)
    
    plt.xlabel('date')
    plt.ylabel('number of mentions')
    title = 'Frequency of topic mentions by date: ' + labelStr
    plt.title(title, fontsize=16, fontweight='bold')
    
    plt.plot(x,y, label=labelStr, color="blue")
    plt.legend(loc='upper right')
    
    ax.xaxis.set_major_locator(plt.MaxNLocator(9))
    filename = labelStr + '_frequency_plot.png'
    fig.savefig(filename)