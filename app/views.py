from flask import render_template, request
from app import app
import pymysql as mdb
#from a_Model import ModelIt

#the top languages from repo
languages=[
'C',
'C#',
'C++',
'CoffeeScript',
'CSS',
'Go',
'HTML',
'Java',
'Javascript',
'Objective-C',
'PHP',
'Perl',
'Python',
'R',
'Ruby',
'Scala',
'Shell',
'Swift',
'TeX',
'VimL']

@app.route('/')
@app.route('/index')
@app.route('/input')
def git_input():

    return render_template("index.html", month="September", languages=languages)

@app.route('/output_one')
def output_one():

    Name1 = request.args.get('Name1')
    if not Name1:
        Name1 = 'scikit-learn/scikit-learn'

    db = mdb.connect(host='localhost',user='hebda',db='joined',charset='utf8')
    with db:
        cur = db.cursor()
        cur.execute("SELECT * FROM repo WHERE name=%s;" % Name1)


    ## Check if inputs correspond to valid schools
    schools1 = query_past_scores(None, name=Name1)
    schools2 = query_past_scores(None, name=Name2)

    if (not schools1) or (not schools2):
        return render_template('error.html')
        

@app.route('/input_list')
def input_list():
    return render_template("index.html", month="September", languages=languages)

@app.route('/index_again')
def index_again():
    return render_template("index.html#select_list", month="September", languages=languages)

@app.route('/index_one')
def input_one():

    name_list=[]
    db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')
    with db:
        cur=db.cursor()
        cur.execute("SELECT name FROM repo WHERE status=1")
        name_list=sorted(list(set([i[0] for i in cur.fetchall()] )))

    return render_template("index_one.html", name_list=name_list, month="September", languages=languages)

@app.route('/output_list')
@app.route('/output')
def output_list():
  #pull 'name' from input field and store it
  description_tag = request.args.get('description_tag')
  hotness = request.args.get('hotness')
  language_list=[]
  for i in languages:
      if request.args.get(i)==i:
          language_list.append(i)


  db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')
  with db:
    cur = db.cursor()

    where_clause="WHERE status=1 AND pred1 IS NOT NULL"
    if hotness=='hotness':
        where_clause+=" AND hot=1"
    if len(language_list)>0:
        where_clause+=" AND (language=\"%s\"" % language_list[0]
        for i in language_list[1:]:
            where_clause+=" OR language=\"%s\"" % i
        where_clause+=")"

    cur.execute("SELECT id,name,description,language,watchers,pred1,pred2,hot FROM repo %s ORDER BY pred1 DESC LIMIT 10;" % where_clause )

    result_list=list(cur.fetchall())
    for i in range(len(result_list)):
        result_list[i]=list(result_list[i])
        result_list[i][2]=result_list[i][2].replace('?','')

    monthly_results=[]
    #for i in result_list:
    #    repoid=i[0]
    #    cur.execute("SELECT CASE WHEN timestamp BETWEEN '2015-06-01' AND '2015-06-30' THEN 'june' WHEN timestamp BETWEEN '2015-07-01' AND '2015-07-31' THEN 'july' WHEN timestamp BETWEEN '2015-08-01' AND '2015-08-31' THEN 'august' WHEN timestamp BETWEEN '2015-09-01' AND '2015-09-30' 'september ELSE 'october' END AS month, count(type) AS num_events FROM event WHERE type=17 and id=%d GROUP BY month;" % repoid)
    #
    #    hist_push = {}
    #    for result in cur.fetchall():
    #        hist_push[result[0]]=result[1]
    #    hist_push['pred']=i[5]
    #
    #    cur.execute("SELECT CASE WHEN timestamp BETWEEN '2015-06-01' AND '2015-06-30' THEN 'june' WHEN timestamp BETWEEN '2015-07-01' AND '2015-07-31' THEN 'july' WHEN timestamp BETWEEN '2015-08-01' AND '2015-08-31' THEN 'august' WHEN timestamp BETWEEN '2015-09-01' AND '2015-09-30' 'september ELSE 'october' END AS month, count(type) AS num_events FROM event WHERE type=19 and id=%d GROUP BY month;" % repoid)
    #    hist_watch={}
    #    for result in cur.fetchall():
    #        hist_watch[result[0]]=result[1]
    #    hist_watch['pred']=i[6]
    #
    #    for month in ['june','july','august','september','october']:
    #        if month not in hist_push:
    #            hist_push[i]=0
    #        if month not in hist_watch:
    #            hist_watch[i]=0

  #call a function from a_Model package. note we are only pulling one result in the query
  #pop_input = cities[0]['population']
  #the_result = ModelIt(city, pop_input)
  the_result=0
  return render_template("index.html", the_result = result_list, display_list_result=1, languages=languages, language_checklist=language_list, hotness=hotness)

@app.route('/slides')
def slides():
    return render_template('slides.html')

@app.route('/error')
def error():
    return render_template('error.html')

