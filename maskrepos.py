#!/usr/bin/env python

import json
import os, sys
import pymysql as mdb
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


# Read a dataset
d=pd.read_csv('data/application_set_august.csv',header=None,index_col=False)

#in case of crash, skip these lines
skip_lines=0

#d.iloc[:,range(40)+[58]]
d.columns = ['id']+range(60)
d.index = d['id']
d=d.drop('id',1)
d_full=d

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
    event_req = ((d.ix[:,20:59]>0).sum(1)>7) & (d.ix[:,[33,34,35,53,54,55]].sum(1)>=2)
    event_req = (tot1>=100) & (tot2>=100)

    for i in range(d.shape[0])[skip_lines:]:
        
        repoid=d.index[i]
        #print repoid
        status=3
        if not event_req[repoid]:
            print repoid
            #cur.execute('UPDATE repo SET status=%d WHERE id=%d' % (status,repoid) )

    cur.close()
db.close()    

