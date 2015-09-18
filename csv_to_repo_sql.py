#!/usr/bin/env python


import pymysql as mdb
db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')

filename='data/repo.csv'

with db:
    cur = db.cursor()

    with open(filename) as f:
        for line in f:

            repoid=line.replace('(','').replace('\n','').split(',')[0]

            #if repoid not in db, create entry
            #if cur.execute('SELECT COUNT(id) FROM repo WHERE id=%s GROUP BY id' % repoid) ==0:
             
            cur.execute('INSERT INTO repo (id, name) VALUES %s' % ( line ) )



