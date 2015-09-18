from flask import render_template, request
from app import app
import pymysql as mdb
from a_Model import ModelIt

db = mdb.connect(user="hebda", host="localhost", db="GitWatch", charset='utf8')

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')
def cities_page():
    with db:
        cur = db.cursor()
        cur.execute("SELECT Name FROM City LIMIT 15;")
        query_results = cur.fetchall()
    cities = ""
    for result in query_results:
        cities += result[0]
        cities += "<br>"
    return cities

@app.route("/db_fancy")
def cities_page_fancy():
    with db:
        cur = db.cursor()
        cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population LIMIT 15;")

        query_results = cur.fetchall()
    cities = []
    for result in query_results:
        cities.append(dict(name=result[0], country=result[1], population=result[2]))
    return render_template('cities.html', cities=cities)

@app.route('/input')
def cities_input():
  return render_template("input.html")

@app.route('/output')
def cities_output():
  #pull 'name' from input field and store it
  reponame = request.args.get('ID')

  with db:
    cur = db.cursor()
    #just select the city from the world_innodb that the user inputs
    cur.execute("SELECT CASE WHEN timestamp BETWEEN '2015-06-01' AND '2015-06-30' THEN 'june' WHEN timestamp BETWEEN '2015-07-01' AND '2015-07-31' THEN 'july' WHEN timestamp BETWEEN '2015-08-01' AND '2015-08-31' THEN 'august' ELSE 'september' END AS month, count(type) AS num_events FROM repo,event  WHERE repo.id=event.id and repo.name=\"%s\" GROUP BY month;" % reponame)

    query_results = cur.fetchall()

  nums = {}
  for result in query_results:
      nums[result[0]]=result[1]
      #nums.append(dict(month=result[0], num_events=result[1]))
    
  for i in ['june','july','august','september']:
      if i not in nums:
          nums[i]=0

  #call a function from a_Model package. note we are only pulling one result in the query
  #pop_input = cities[0]['population']
  #the_result = ModelIt(city, pop_input)
  the_result=0
  return render_template("output.html", nums = nums, the_result = the_result)
