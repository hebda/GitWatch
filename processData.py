#!/usr/bin/env python

import numpy as np
import pandas as pd
import datetime, date, time
from nltk.stem.porter import *

stoptime=datetime.datetime.combine(date(2015,1,2),time(0,0,0))
stemmer = PorterStemmer()

#get features
features=[]
f=open('features_dict.info','r')
for line in f.readlines():
    features.append(line.replace('\n',''))
f.close()

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

    words=''.join([i if ord(i)>=97 and ord(i)<122 else ' ' for i in message.replace('\n',' ').lower()]).split()
    words=[stemmer.stem(i) for i in words]

    for i in words:
        if i in features:
            

text.close()
