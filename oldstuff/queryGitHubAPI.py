#!/usr/bin/env python

import json
import os, sys
import pymysql as mdb

token=sys.argv[1]
limit=5000
#store result of SELECT id, count(*) AS num_events FROM events GROUP BY id ORDER BY num_events DESC;
#in data/cache_results.txt

os.system('head -n %d data/repo_events.csv > process.tmp' % limit)
os.system('tail -n +%d data/repo_events.csv > remainder.txt' % limit+1 )
os.system('mv remainder.txt data/repo_events.csv')

repoids=[]
with open('process.tmp','r') as f:

    repoids=[]
    for i in f:
        repoid=int(i.split(',')[0])
        repoids.append(repoid)

for repoid in repoids:
    
    tmpfile="repo_info/tmpjson_%s" % repoid

    status=os.system('wget -O %s https://api.github.com/repositories/%d?access_token=86e4b6b7e573c30543a27243e7459c04d6683c80' % (tmpfile,repoid))

    filesize=int(os.popen('cat %s | wc -c' % tmpfile).read().replace('\n',''))
    if filesize==0:
        print "Error in downloading. Probably a private repo."
        os.system('echo %d >> retry.txt' % repoid)
        os.system('rm %s' % tmpfile)

os.system('rm process.tmp')

