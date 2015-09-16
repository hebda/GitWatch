#!/usr/bin/env python

import datetime
stoptime=datetime.datetime.combine(datetime.date(2015,2,1),datetime.time(0,0,0))

repoids={}

text=open('data/text.csv','r')

for line in text:

    vec=line.split(',',4)
    eventid=int(vec[0])
    repoid=int(vec[1])
    actorid=int(vec[2]) #not used
    timestamp=datetime.datetime.strptime(vec[3], '%Y-%m-%dT%H:%M:%SZ')
    message=vec[4]

    if timestamp.minute==0 and timestamp.second==0:
        print timestamp
    if timestamp > stoptime:
        break

    if repoid in repoids:
        repoids[repoid]+=1
    else:
        repoids[repoid]=1

text.close()

print len(repoids)

ctr=0
for i in repoids:
    ctr+=repoids[i]
print ctr
