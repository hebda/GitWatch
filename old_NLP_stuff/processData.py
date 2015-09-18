#!/usr/bin/env python

import numpy as np
import pandas as pd
import datetime as datetime
from nltk.stem.porter import *
import random as rand

stoptime=datetime.datetime.combine(datetime.date(2015,1,10),datetime.time(0,0,0))
stemmer = PorterStemmer()

rand.seed(2468)

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
class_dict={} #class label
num_ct_features=16

#there is too much data. take 1k repos for now.
num_accept=1000
num_jan=392899 #for first 10 days. 999268 num repos in all january
repo_accept=[]
repo_reject=[]

## Summary of the 16 countable features:
# name in json, id in extracted file, index herein
# PushEvent 0 0
# CommitCommentEvent 1 1
# IssueCommentEvent 2 2
# IssuesEvent 3 3
# PullRequestReviewCommentEvent 4 4
# CreateEvent 5-branch 5
# CreateEvent 5-tag 6
# DeleteEvent 6-branch 7
# DeleteEvent 6-tag 8
# MemberEvent 7-added 9
# MembershipEvent 8 -
# PublicEvent 9 10
# PullRequestEvent 10-opened 11
# PullRequestEvent 10-closed 12
# PullRequestEvent 10-reopened 13
# ReleaseEvent 11 14
# StatusEvent 12 -
# TeamAddEvent 13 -
# WatchEvent 14 15

#now run on data
text=open('data/text.csv')
for line in text:

    vec=line.split(',',4)
    eventid=int(vec[0])
    repoid=int(vec[1])
    actorid=int(vec[2]) #not used
    timestamp=datetime.datetime.strptime(vec[3], '%Y-%m-%dT%H:%M:%SZ')
    message=vec[4]

    if timestamp.minute==0 and timestamp.second==0:
        print timestamp
    if timestamp > stoptime:
        break
    if repoid in repo_reject:
        continue
    elif repoid not in repo_accept:
        if rand.randint(1,num_jan)<=num_accept:
            repo_accept.append(repoid)
        else:
            repo_reject.append(repoid)
            continue


    event_vec=np.zeros(num_ct_features,int)
    event_vec[eventid]=1
    time_vec=np.array([int((timestamp-datetime.datetime(2010,1,1,0,0,0)).total_seconds())],int)
    words=''.join([i if ord(i)>=97 and ord(i)<122 else ' ' for i in message.replace('\n',' ').lower()]).split()
    word_list=[stemmer.stem(i) for i in words]
    word_vec=np.zeros(len(word_features),int)
    for i in word_list:
        if i in word_features:
            word_index=word_features.index(i)
            word_vec[word_index]+=1

    new_entry=np.concatenate((time_vec,event_vec,word_vec))


    if eventid==0:#this is a commit message. copy lc and rfalc into repo_features. strore message in lc.
        if repoid not in repo_features:
            repo_features[repoid]=np.concatenate((time_vec,np.zeros(num_ct_features,int),np.zeros(len(word_features),int)))
        if repoid in lc:
            repo_features[repoid][1:]=repo_features[repoid][1:]+lc[repoid][1:]
        lc[repoid]=new_entry
        class_dict[repoid]=('fix' in word_list or 'bug' in word_list or 'bugfix' in word_list)
        if repoid in rfalc:
            repo_features[repoid][1:]=repo_features[repoid][1:]+rfalc[repoid]
            del rfalc[repoid]
    else:#do not change timestamp
        if repoid in rfalc:
            rfalc[repoid]=rfalc[repoid]+new_entry[1:]
        else:
            rfalc[repoid]=new_entry[1:]

text.close()

events=open('data/events.csv','r')

for line in events:

    vec=line.split(',',4)
    eventid=int(vec[0])
    repoid=int(vec[1])
    actorid=int(vec[2]) #not used
    timestamp=datetime.datetime.strptime(vec[3], '%Y-%m-%dT%H:%M:%SZ')
    message=vec[4].replace('\n','')

    if timestamp > stoptime:
        break

    if repoid not in repo_features:
        continue

    eventid_translated=-1
    if eventid==5 and message=='branch':
        eventid_translated=5
    elif eventid==5 and message=='tag':
        eventid_translated=6
    elif eventid==6 and message=='branch':
        eventid_translated=7
    elif eventid==6 and message=='tag':
        eventid_translated=8
    elif eventid==7:
        eventid_translated=9
    elif eventid==9:
        eventid_translated=10
    elif eventid==10 and message=='opened':
        eventid_translated=11
    elif eventid==10 and message=='closed':
        eventid_translated=12
    elif eventid==10 and message=='reopened':
        eventid_translated=13
    elif eventid==11:
        eventid_translated=14
    elif eventid==14:
        eventid_translated=15

    if eventid_translated<5:
        continue

    #scale eventid_translated to correspond directly with index in array
    eventid_translated+=1

    time_sec= int((timestamp-datetime.datetime(2010,1,1,0,0,0)).total_seconds())
    if repo_features[repoid][0] > time_sec:
        repo_features[repoid][eventid_translated]+=1

events.close()


processed_csv=open('processed.csv','w')
for i in repo_features:
    outline='%d,' % i
    for j in repo_features[i]:
        outline+='%d,' % j
    outline+='%d\n' % class_dict[i]
    processed_csv.write(outline)

processed_csv.close()
#output is repoid,time,16 event counts,word vector,class label 
