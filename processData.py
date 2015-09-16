#!/usr/bin/env python

import numpy as np
import pandas as pd
import datetime, date, time
from nltk.stem.porter import *


stoptime=datetime.datetime.combine(date(2015,1,2),time(0,0,0))
stemmer = PorterStemmer()

#get word features
word_features=[]
f=open('features_dict.info','r')
for line in f.readlines():
    word_features.append(line.replace('\n',''))
f.close()

#repo attributes are stored in repo_features
#since training/testing/validation will be performed on the last commit, another structure is needed.
repo_features={}
rfalc={} #repo features after last commit
lc={} #last commit

#now run on data
text=open('text.csv')
for line in text:

    vec=line.split(',',4)
    eventid=int(vec[0])
    repoid=int(vec[2])
    timestamp=datetime.strptime(vec[3], '%Y-%m-%dT%H:%M:%SZ')
    message=vec[4]

    if timestamp > stoptime:
        break

    event_vec=np.zeros(5,int)
    event_vec[eventid]=1
    time_vec=np.array([int((timestamp-datetime.datetime(2010,1,1,0,0,0)).total_seconds())],int)
    words=''.join([i if ord(i)>=97 and ord(i)<122 else ' ' for i in message.replace('\n',' ').lower()]).split()
    word_list=[stemmer.stem(i) for i in words]
    word_vec=np.zeros(len(word_features),int)
    for i in word_list:
        if i in word_features:
            word_index=word_list.index(i)
            word_vec[word_index]=word_vec[word_index]+1

    new_entry=np.concatenate((time_vec,event_vec,word_vec))


    if eventid==0:#this is a commit message. copy lc and rfalc into repo_features. strore message in lc.
        if repoid not in repo_features:
            repo_features[repoid]=np.concatenate((time_vec,np.zeros(5,int),np.zeros(len(word_features),int)))            
        if repoid in lc:
            repo_features[repoid][1:]=repo_features[repoid][1:]+lc[repoid][1:]
        lc[repoid]=new_entry
        if repoid in rfalc:
            repo_features[repoid][1:]=repo_features[repoid][1:]+rfalc[repoid][1:]
            del rfalc[repoid]
    else:#do not change timestamp
        if repoid in rfalc:
            rfalc[repoid]=rfalc[repoid]+new_entry[1:]
        else:
            rfalc[repoid]=new_entry[1:]


text.close()



#now assign labels
