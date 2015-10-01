#!/usr/bin/env python

import os, sys
import pymysql as mdb
import numpy as np

skip_lines=0

start_month=8 #Use Aug, Sep to predict Oct

db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8', autocommit=True)

with db:

    cur = db.cursor()

    #This file is populated by:
    #SELECT id,COUNT(*) AS num FROM event GROUP BY id;
    with open('data/training_repos.csv','r') as f_in:

        ctr=0
        for i in f_in:

            if ctr<skip_lines:
                ctr+=1
                continue

            repoid=int(i.split(',')[0])
            events=int(i.split(',')[1].replace('\n',''))

            with open('data/application_set.csv','a') as f_out:

                print "Processing repoid %d (%d events)" % (repoid,events)
                cur.execute('SELECT type,timestamp FROM event WHERE id=%d and timestamp<"2015-10-01" and timestamp>"2015-06-30"' % repoid)
                event_info=np.zeros(60,int)

                for j in cur.fetchall():

                    index=j[0]+20*(j[1].month-start_month)
                    if index < 0 or index>=60:
                        continue

                    event_info[index]+=1

                f_out.write(str(repoid)+','+','.join(['%d' % num for num in event_info])+'\n')

    cur.close()
db.close()    

