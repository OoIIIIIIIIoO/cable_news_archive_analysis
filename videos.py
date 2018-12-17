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

#converts a string in the format HOURS:MINUTES:SECONDS to seconds
def time_to_seconds(time):
    seconds = 60*60*int(time[0:2])+ 60*int(time[3:5])+ int(time[6:8])
    return seconds

#displays a video in the <video src="https://storage.cloud.google.com/esper/tvnews/videos/{item_name}.mp4#t={time}" 
# link given a filename and the time
def show_video(item_name, time):
    display(HTML("""
    <video src="https://storage.cloud.google.com/esper/tvnews/videos/{item_name}.mp4#t={time}" 
      autoplay
      controls
      />
    """.format(item_name=item_name, time=time)))

#displays a vidoe given a segment object that holds information on the file, start time and end time of the videos.
def show_video_segment(segment):
    name = segment.file[:len(segment.file)-8]
    start_time = time_to_seconds(segment.start_time)
    end_time = time_to_seconds(segment.end_time)
    print('Video: ', name)
    print('Time:', segment.start_time, ' - ', segment.end_time)
    show_video(name, start_time - 5 )