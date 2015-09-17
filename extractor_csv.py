#!/usr/bin/env python

import json
import sys
#import pymysql as mdb
#db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')

type_dict = {
    'CommitCommentEvent':0,
    'CreateEvent':1, #two types: branch and tag
    'DeleteEvent':3, #two types: branch and tag
    'ForkEvent':5,
    'GollumEvent':6,
    'IssueCommentEvent':7,
    'IssuesEvent':8, #three types: opened, closed, reopened
    'MemberEvent':11,
    'PublicEvent':12,
    'PullRequestEvent':13, #three types: opened, closed, reopened
    'PullRequestReviewCommentEvent':16,
    'PushEvent':17,
    'ReleaseEvent':18,
    'WatchEvent':19,
}

repofile=open('repo.csv','a')

with open('event.csv','a') as eventfile:
    #cur = db.cursor()

    with open(sys.argv[1]) as f:
        for line in f:
            data=(json.loads(line))
            datatype=data['type']

            repoid=data['repo']['id']
            eventid=-1
            timestamp=data['created_at'].replace('Z','').replace('T',' ')

            if datatype in type_dict:
                eventid=type_dict[datatype]
                if eventid==1 or eventid==3:
                    if data['payload']['ref_type']=='tag':
                        eventid+=1
                    elif data['payload']['ref_type']!='branch':
                        eventid=-1
                elif eventid==8 or eventid==13:
                    if data['payload']['action']=='opened':
                        eventid+=1
                    elif data['payload']['action']=='reopened':
                        eventid+=2
                    elif data['payload']['action']!='closed':
                        eventid=-1

            if eventid<0:
                continue

            # add entry into event db
            #cur.execute('INSERT INTO event VALUES (%d,%d,"%s")' % (repoid,
            #                                                     eventid,
            #                                                     timestamp ) )

            #if repoid not in db, create entry
            #if cur.execute('SELECT COUNT(id) FROM repo WHERE id=%d GROUP BY id' % repoid) ==0:
            #    cur.execute('INSERT INTO repo (id, name) VALUES (%d,"%s")' % (repoid,
            #                                                                  data['repo']['name'] ))
            #elif datatype=='WatchEvent': # if id not in repo table, nothing will happen.
            #    cur.execute('UPDATE repo SET watchers=watchers+1 WHERE id=%d' % repoid )
            #    print "Watchers in repoid %d went up by 1.\n" % repoid

            eventfile.write('(%d,%d,\"%s\")\n' % (repoid, eventid, timestamp) )
            repofile.write(('(%d,\"%s\")\n') % (repoid, data['repo']['name']) )

repofile.close()
