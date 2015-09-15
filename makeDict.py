#!/usr/bin/env python

import datetime
from nltk.stem.porter import *
import operator

text=open('text.csv','r')
#run for 1 month
stoptime=datetime.datetime.combine(datetime.date(2015,2,1),datetime.time(0,0,0)) 

features=dict()
stemmer = PorterStemmer()

for line in text:

    vec=line.split(',',4)
    eventid=int(vec[0])
    repoid=int(vec[2])
    timestamp=datetime.datetime.strptime(vec[3], '%Y-%m-%dT%H:%M:%SZ')
    message=vec[4]

    if timestamp > stoptime:
        break

    words=''.join([i if ord(i)>=97 and ord(i)<122 else ' ' for i in message.replace('\n',' ').lower()]).split()

    for i in words:
        stemmed_i=stemmer.stem(i)
        if stemmed_i in features:
            features[stemmed_i]=features[stemmed_i]+1
        else:
            features[stemmed_i]=1

text.close()

#still requires manual pruning
output=open('features_dict.info','w')
sorted_features=sorted(features.items(),key=operator.itemgetter(1),reverse=True)
for i in range(2000):
    output.write(sorted_features[i][0]+'\n')
output.close()
