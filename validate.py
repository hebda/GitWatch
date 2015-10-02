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
d_sep=pd.read_csv('data/application_set_september.csv',header=None,index_col=False)
d_aug=pd.read_csv('data/application_set_september.csv',header=None,index_col=False)

d_sep.columns = ['id']+range(60)
d_sep.index = d_sep['id']
d_sep=d_sep.drop('id',1)
d_aug.columns = ['id']+range(60)
d_aug.index = d_aug['id']
d_aug=d_aug.drop('id',1)

clf1 = joblib.load('training/gradientboostedregression_pushes.pkl')
lr1  = joblib.load('training/linearregression_pushes.pkl')
clf2 = joblib.load('training/gradientboostedregression_watches.pkl')

#require each repo to have at least 100 events in months 1,2
#require each repo to have more than 7 types of activity
#require each repo to have at least 2 PR events
tot1_sep=d_sep.ix[:,0:20].sum(1)
tot2_sep=d_sep.ix[:,20:40].sum(1)
tot3_sep=d_sep.ix[:,40:60].sum(1)
event_req_sep = ((d_sep.ix[:,range(40)]>0).sum(1)>7) & (d_sep.ix[:,[13,14,15,33,34,35]].sum(1)>=2) & (tot1_sep>=100) & (tot2_sep>=100)
tot1_aug=d_aug.ix[:,0:20].sum(1)
tot2_aug=d_aug.ix[:,20:40].sum(1)
tot3_aug=d_aug.ix[:,40:60].sum(1)
event_req_aug = ((d_aug.ix[:,range(40)]>0).sum(1)>7) & (d_aug.ix[:,[13,14,15,33,34,35]].sum(1)>=2) & (tot1_aug>=100) & (tot2_aug>=100)

event_req = event_req_aug & event_req_sep

res1 = clf1.predict(d_sep.ix[:,range(40)])
res1[res1<0]=0
res2 = lr1.predict(d_sep.ix[:,[13,14,17,33,34,37]])
res2[res2<0]=0
res3 = np.array(d_sep.ix[:,37])
res_pushes=(res1+res2+res3)/3.
res_watchers = clf2.predict(d_sep.ix[:,range(40)])
res_watchers[res_watchers<0]=0

f_out = open('validation_output.txt','w')

for i in range(d_sep.shape[0]):
        
    repoid=d_sep.index[i]

    if not event_req[repoid]:
        continue

    pred1=int(round(res_pushes[i]))
    pred2=int(round(res_watchers[i]))
    hipster=(res_watchers[i]>d_sep.ix[repoid,39]*2+10)

    true1=d_sep.ix[repoid,57]
    true2=d_sep.ix[repoid,59]
    hipster_true=(true2>d_sep.ix[repoid,39]*2+10)

    f_out.write("%d %d %d %d %d %d %d" % (repoid, pred1, true1, pred2, true2, hipster, hipster_true) )

f_out.close()
