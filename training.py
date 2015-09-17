#!/usr/bin/env python

import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB

#get word features
word_features=[]
f=open('features_dict.info','r')
for line in f.readlines():
    word_features.append(line.replace('\n',''))
f.close()

gnb = GaussianNB()

df=pd.read_csv('processed.csv',header=None)
num_entries=len(df)

df_train=df[0:num_entries/2]
df_test=df[num_entries:]

y_pred = gnb.fit(df_train[df_train.columns[2:-1]], df_train[1017]).predict(df_test[df_test.columns[2:-1]])

print (y_pred != df_test[1017]).sum()
#iris.data.shape[0],(iris.target != y_pred).sum())

