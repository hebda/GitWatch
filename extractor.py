#!/usr/bin/env python

import json
import sys
import pymysql as mdb
#db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')

type_dict = {
    'PushEvent':0,
    'CommitCommentEvent':1,
    'IssueCommentEvent':2,
    'IssuesEvent':3,
    'PullRequestReviewCommentEvent':4,
    'CreateEvent':5,
    'DeleteEvent':6,
    'MemberEvent':7,
    'MembershipEvent':8, #does not exist
    'PublicEvent':9,
    'PullRequestEvent':10,
    'ReleaseEvent':11,
    'StatusEvent':12, #does not exist
    'TeamAddEvent':13, #does not exist
    'WatchEvent':14
}

#line info: repoid, event, time, message, other

with open('events.csv','a') as output:
#with db:
    #cur = db.cursor()
    #cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population LIMIT 15;")

    with open(sys.argv[1]) as f:
        for line in f:
            data=(json.loads(line))
            datatype=data['type']

            repoid=data['repo']['id']
            eventid=-1
            timestamp=data['created_at'].replace('Z','').replace('T',' ')
            message=''
            other=0

            if datatype=='PushEvent':
                eventid=0
                numCommits=0
                for i in range(len(data['payload']['commits'])):
                    numCommits+=1
                    message+="%s " % data['payload']['commits'][i]['message'].replace('\n',' ')
                message=message[:-1]
                other=numCommits
                if other==0:
                    continue

            elif datatype=='CommitCommentEvent':
                eventid=1
                message=data['payload']['comment']['body'].replace('\n',' ')
            elif datatype=='IssueCommentEvent': # not using not using data['payload']['action'] in issues
                eventid=2
                message=data['payload']['comment']['body'].replace('\n',' ')
            elif datatype=='IssuesEvent': # not using not using data['payload']['action'] in issues
                eventid=3
                message=data['payload']['issue']['title'].replace('\n',' ')
            elif datatype=='PullRequestReviewCommentEvent':
                eventid=4
                message=data['payload']['comment']['body'].replace('\n',' ')
            elif datatype=='CreateEvent':
                if data['payload']['ref_type']=='branch':
                    eventid=5
                elif data['payload']['ref_type']=='tag':
                    eventid=6
            elif datatype=='DeleteEvent':
                if data['payload']['ref_type']=='branch':
                    eventid=7
                elif data['payload']['ref_type']=='tag':
                    eventid=8
            elif datatype=='MemberEvent':
                eventid=9
            elif datatype=='PublicEvent':
                eventid=10
            elif datatype=='PullRequestEvent':
                if data['payload']['action']=='opened':
                    eventid=11
                elif data['payload']['action']=='closed':
                    eventid=12
                elif data['payload']['action']=='reopened':
                    eventid=13
            elif datatype=='ReleaseEvent':
                eventid=14
            elif datatype=='WatchEvent':
                eventid=15

            if eventid<0:
                continue

            outline="%s,%s,%s,%s,%d\n" % (repoid,eventid,timestamp,message,other)
            output.write(outline.encode('utf-8'))


