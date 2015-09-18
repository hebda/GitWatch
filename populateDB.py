#!/usr/bin/env python

import json
import os, sys
import pymysql as mdb
db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')

clientid=sys.argv[1]
clientsecret=sys.argv[2]

with db:
    cur = db.cursor()

    #if repoid not in db, create entry
    cur.execute('SELECT name FROM repo WHERE status is NULL')

    calls=0
    limit=4900
    for i in cur.fetchall():

        tmpfile="tmpjson_%s" % i[0].replace('/','')
        print 'before download'
        status=os.system('wget -O %s https://api.github.com/repos/%s?client_id=%s&client_secret=%s' % (tmpfile,i[0],clientid,clientsecret))
        os.system('sleep 1')
        print 'after download'
        if status!=0:
            print "Nothing found for %s" % i[0]
            #update db so that status is no longer null
            cur.execute('UPDATE repo SET status=0 WHERE name="%s"' % i[0])
            continue

        with open(tmpfile,'r') as repoinfo:
            jsonfile=' '.join(repoinfo.readlines()).replace('\n','')
            data=json.loads(jsonfile)

            repoid=data['id']
            private=data['private']
            created_at=data['created_at'].replace('Z','').replace('T',' ')
            desc=data['description']
            lang=data['language']
            watchers=data['watchers']

            status=cur.execute('UPDATE repo SET private=%d, created_at="%s", description="%s", language="%s", watchers=%d, status=1 WHERE id=%d;' % ( private, created_at, desc, lang, watchers, repoid ))

        os.system('rm %s' % tmpfile)

        calls+=1
        if calls>=limit:
            break
