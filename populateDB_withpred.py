#!/usr/bin/env python

import json
import os, sys
import pymysql as mdb
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
from string import letters
from sklearn.externals import joblib

sns.set(style="white")

# Read a dataset
d=pd.read_csv('data/application_set.csv',header=None,index_col=False)

#d.iloc[:,range(40)+[58]]
d.columns = ['id']+range(60)
d.index = d['id']
d=d.drop('id',1)
d_full=d

clf1 = joblib.load('training/gradientboostedregression_pushes.pkl')
lr1  = joblib.load('training/linearregression_pushes.pkl')
clf2 = joblib.load('training/gradientboostedregression_watches.pkl')

db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8', autocommit=True)

with db:

    cur = db.cursor()

    #require each repo to have at least 100 events in months 1,2
    #require each repo to have more than 7 types of activity
    #require each repo to have at least 2 PR events
    tot1=d.ix[:,0:20].sum(1)
    tot2=d.ix[:,20:40].sum(1)
    tot3=d.ix[:,40:60].sum(1)
    event_req = ((d.ix[:,range(40)]>0).sum(1)>7) & (d.ix[:,[13,14,15,33,34,35]].sum(1)>=2)
    event_req = event_req & (tot1>=100) & (tot2>=100)

    res1 = clf1.predict(d.ix[:,range(40)])
    res1[res1<0]=0
    res2 = lr1.predict(d.ix[:,[13,14,17,33,34,37]])
    res2[res2<0]=0
    res3 = np.array(d.ix[:,37])
    res_pushes=(res1+res2+res3)/3.
    res_watchers = clf2.predict(d.ix[:,range(40)])
    res_watchers[res_watchers<0]=0

    for i in range(d.shape[0]):
        
        repoid=d.index[i]
        print repoid
        pred1=int(round(res_pushes[i]))
        pred2=int(round(res_watchers[i]))
        hot=(res_watchers[i]>d.ix[repoid,39]*2+10)
        status=0
        if event_req[repoid]:
            status=1
        else:
            status=2

        cur.execute('UPDATE repo SET status=%d,pred1=%d,pred2=%d,hot=%d WHERE id=%d' % (status,pred1,pred2,hot,repoid) )

    cur.close()
db.close()    

