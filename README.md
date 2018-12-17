# cable_news_archive_analysis

This project was developed for a computational journalism class at Stanford (CS206) 
This repository contains the code for our project and our project's results. 

The goal was to analyze cable news transcripts by writing topic modelling, sentiment analysis and bias 
recognition algorithms. We analyzed the 2016 pre (presidential) election period and the 2018 pre midterm 
election period. Unfortunatley we are do not have permission to upload the cable news transcripts. 

CONTENTS:
-The 'cable news archive essay.pdf' is a paper that explains our project and summarises our methods and conclusions.

-The 'Data Mining Cable News Transcripts Presentation.pdf' file contains the slides of our project’s presentation including 
a lot of our data analysis and our graphs. 

-The 'topic_modelling' file contains functions for topic modelling, sentiment analysis, bias classification 
and lexicon generation. The functions that end in '_transcripts' are to be used with files of transcripts in 
the format used by the internet archive. The functions that end in '_text' are for plain text. 

-The 'modules_comp_journ; file contains some of the helper functions for the topic modelling file. The file_parsing file 
contains parsing functions that are called from the topic modelling file.

The printing file has functions that are responsible for printing out things returned by the topic modelling functions. 

The graphs file handles visualisations of the outputs of the functions in the topic modelling file - graphs of frequency 
of mentions, sentiment, bias.

Lastly, the videos file contains functions that can be called on segments outputted by the topic modelling functions. 
The functions in this file are responsible for displaying the news tv segments that correspond to the segments outputted 
by the topic modelling functions. The videos cannot be displayed without authorisation. 
