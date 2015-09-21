#!/usr/bin/env python

import json
import os, sys
import pymysql as mdb

token=sys.argv[1]

db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8', autocommit=True)

with db:

    cur = db.cursor()
    with open('data/repo_events.csv','r') as f:

        for i in f:
            repoid=int(i.split(',')[0])

            action=""
            num_entries=cur.execute('SELECT id FROM repo WHERE id=%d' % repoid)
            if num_entries==0:
                action='insert'
            elif num_entries>1:
                cur.execute('DELETE FROM repo WHERE id=%d' % repoid )
                action='insert'
            elif cur.execute('SELECT id FROM repo WHERE id=%d and status is NULL' % repoid)>0:
                action='update'
            else:
                continue

            tmpfile="tmpjson_%s" % repoid
            print "%s item %d" % (action,repoid)

            #status=os.system('wget -O %s https://api.github.com/repos/%s?client_id=%s&client_secret=%s' % (tmpfile,i[0],clientid,clientsecret))
            status=os.system('wget -O %s https://api.github.com/repositories/%d?access_token=%s' % (tmpfile,repoid,token))

            filesize=int(os.popen('cat %s | wc -c' % tmpfile).read().replace('\n',''))
            if status!=0:
                print "Nothing found for %s" % repoid
                #update db so that status is no longer null
                if action=='insert':
                    cur.execute('INSERT INTO repo (id,private,status) VALUES (%d,1,0)' % repoid )
                elif action=='update':
                    cur.execute('UPDATE repo SET private=1, status=0 WHERE id=%d' % repoid )
                os.system('rm %s' % tmpfile)
            elif filesize==0:
                print "Error in downloading. Try again later."
            else:
                with open(tmpfile,'r') as repoinfo:
                    jsonfile=' '.join(repoinfo.readlines()).replace('\n','')
                    data=json.loads(jsonfile)

                    #repoid=data['id']
                    name=data['full_name']
                    private=data['private']
                    created_at=data['created_at'].replace('Z','').replace('T',' ')
                    desc=data['description']
                    if desc is None:
                        desc=""
                    else:
                        desc=desc.replace('"','').replace("'",'').replace('\\','')
                    lang=data['language']
                    if lang is None:
                        lang=""
                    watchers=data['watchers']

                    if action=='insert':
                        cur.execute('INSERT INTO repo (id,name,private,created_at,description,language,watchers,status) VALUES (%d,"%s",%d,"%s","%s","%s",%d,1);'
                                    % (repoid,name,private,created_at,desc,lang,watchers ))
                    elif action=='update':
                        cur.execute('UPDATE repo SET name="%s",private=%d,created_at="%s",description="%s",language="%s",watchers=%d,status=1 WHERE id=%d;'
                                    % (name,private,created_at,desc,lang,watchers,repoid ))

                os.system('rm %s' % tmpfile)

    cur.close()
db.close()    

