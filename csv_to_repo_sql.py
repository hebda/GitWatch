#!/usr/bin/env python


import pymysql as mdb
db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')

filename='repo.csv'

with db:
    cur = db.cursor()

    with open(filename) as f:
        for line in f:

            repoid=line.replace('(','').replace('\n','').split(',')[0]

            #if repoid not in db, create entry
            if cur.execute('SELECT COUNT(id) FROM repo WHERE id=%s GROUP BY id' % repoid) ==0:
                cur.execute('INSERT INTO repo (id, name) VALUES %s' % ( line ) )

            #elif datatype=='WatchEvent': # if id not in repo table, nothing will happen.
            #    cur.execute('UPDATE repo SET watchers=watchers+1 WHERE id=%d' % repoid )
            #    print "Watchers in repoid %d went up by 1.\n" % repoid



