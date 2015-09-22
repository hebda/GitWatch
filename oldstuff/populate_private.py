#!/usr/bin/env python

import json
import os, sys
import pymysql as mdb


#store result of SELECT id, count(*) AS num_events FROM events GROUP BY id ORDER BY num_events DESC;
#in data/cache_results.txt
db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8',autocommit=True)
cur = db.cursor()
with open('private.txt','r') as f:

    for i in f:
        repoid=int(i.split(',')[0])


        with db:

            if cur.execute('SELECT * FROM repo WHERE id=%d' % repoid ) > 0:
                cur.execute('UPDATE repo SET private=1, status=0 where id=%d' %repoid)
            else:
                cur.execute('INSERT INTO repo (id,private,status) VALUES (%d,1,0)' % repoid)

cur.close()
db.close()
