#!/usr/bin/env python

import json
import sys

textinfo = open('text.csv','a')
eventinfo = open('events.csv','a')

type_dict = {
    'PushEvent':0,
    'CommitCommentEvent':1,
    'IssueCommentEvent':2,
    'IssuesEvent':3,
    'PullRequestReviewCommentEvent':4,
    'CreateEvent':5,
    'DeleteEvent':6,
    'MemberEvent':7,
    'MembershipEvent':8,
    'PublicEvent':9,
    'PullRequestEvent':10,
    'ReleaseEvent':11,
    'StatusEvent':12,
    'TeamAddEvent':13,
    'WatchEvent':14
}

with open(sys.argv[1]) as f:
    for line in f:
        data=(json.loads(line))
        datatype=data['type']

        if datatype=='PushEvent':
            for i in range(len(data['payload']['commits'])):
                out_line="%d,%d,%d,%s,%s\n" % (type_dict[datatype],
                                                  data['repo']['id'],
                                                  data['actor']['id'],
                                                  data['created_at'],
                                                  data['payload']['commits'][i]['message'].replace('\n',' '))
                textinfo.write(out_line.encode('utf-8'))

        elif datatype=='CommitCommentEvent' or datatype=='IssueCommentEvent' or datatype=='PullRequestReviewCommentEvent':
            # not using not using data['payload']['action'] in issues
            out_line="%d,%d,%d,%s,%s\n" % (type_dict[datatype],
                                           data['repo']['id'],
                                           data['actor']['id'],
                                           data['created_at'],
                                           data['payload']['comment']['body'].replace('\n',' '))
            textinfo.write(out_line.encode('utf-8'))

        elif datatype=='IssuesEvent':
            # not using not using data['payload']['action'] in issues
            out_line="%d,%d,%d,%s,%s\n" % (type_dict[datatype],
                                           data['repo']['id'],
                                           data['actor']['id'],
                                           data['created_at'],
                                           data['payload']['issue']['title'].replace('\n',' '))
            textinfo.write(out_line.encode('utf-8'))

        elif datatype=='CreateEvent' or datatype=='DeleteEvent':
            out_line="%d,%d,%d,%s,%s\n" % (type_dict[datatype],
                                         data['repo']['id'],
                                         data['actor']['id'],
                                         data['created_at'],
                                         data['payload']['ref_type'])
            eventinfo.write(out_line.encode('utf-8'))
        elif datatype=='MemberEvent' or datatype=='MembershipEvent' or datatype=='PullRequestEvent' or datatype=='WatchEvent':
            out_line="%d,%d,%d,%s,%s\n" % (type_dict[datatype],
                                         data['repo']['id'],
                                         data['actor']['id'],
                                         data['created_at'],
                                         data['payload']['action'])
            eventinfo.write(out_line.encode('utf-8'))
        elif datatype=='PublicEvent' or datatype=='ReleaseEvent' or datatype=='TeamAddEvent':
            out_line="%d,%d,%d,%s,%s\n" % (type_dict[datatype],
                                         data['repo']['id'],
                                         data['actor']['id'],
                                         data['created_at'],
                                         "NA")
            eventinfo.write(out_line.encode('utf-8'))
        elif datatype=='StatusEvent':
            out_line="%d,%d,%d,%s,%s\n" % (type_dict[datatype],
                                         data['repo']['id'],
                                         data['actor']['id'],
                                         data['created_at'],
                                         data['state'])
            eventinfo.write(out_line.encode('utf-8'))


textinfo.close()
eventinfo.close()
