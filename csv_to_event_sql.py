#!/usr/bin/env python


import pymysql as mdb
db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')

filename='data/event.csv'

with db:
    cur = db.cursor()

    with open(filename) as f:
        for line in f:

            # add entry into event db
            cur.execute('INSERT INTO event VALUES %s;' % line.replace('\n','') )

