# GitWatch

GitWatch directs potential contributors to projects on GitHub. This is done by
predicting the future number of pushes and watches of a given repository.
The repositories are ranked in terms of #pushes predicted. The user can toggle
to only show certain languages and/or only repos that will be popular.

### Step 1

Scrape data from the [GitHub Archive](githubarchive.org). This process is very slow.
* Create mySQL tables in the GitWatch database with:
  * `CREATE TABLE repo (id INT UNSIGNED, name TINYTEXT, private BOOL, created_at DATETIME, description TEXT, language TINYTEXT, watchers MEDIUMINT UNSIGNED);`
  * `CREATE TABLE event (id INT UNSIGNED, type TINYINT UNSIGNED, timestamp DATETIME);`
  * `CREATE INDEX id_index ON event (id);` (This will improve lookup performance a lot!)
* `runExtractor.sh` downloads the json that contains all the events for a given hour.
  * `extractor.py` processes the json and records the relevant information in the GitWatch mySQL db.
  * `extractor_csv.py` outputs to file rather than SQL for running remotely. The results are moved to SQL locally with csv_to_{repo,event}_sql.py. Use `sort <filename> | uniq -u` to reduce the size of the `repo.csv` file!
* `populateDB.py` populates the rest of the database info in SQL using GitHub API. The limit is 5k requests / hour with authentication.

### Step 2

Process the data
* `process_training.py` queries sql and creates a csv file for training or applying stuff done in step 3

### Step 3

Training
This was done with the iPython notebook in the directory `training`. Check it out!

### Step 4

Populate training to db. First create three new columns in the repo table for pred1, pred2, hot.
* `process_training.py` creates a table of dimension n(repos) x 60 onto which training can be applied.
* `populateDB_withpred.py` fills in the values
* `maskrepos.py` will impose quality constraints on June and July when applying to October

### Step 5

Run the webapp
* `run.py` will run the web app on the local machine
* `sudo supervisord -c simple.conf` will run the web app on AWS.

## Check out `gitwatch.xyz` to see it run!

### A side note

This project started with the following mission to assign a probability to a given repository
stored on GitHub that the repository contains a bug. The algorithm would have used the previous
commit messages and NLP to assign a probability. The scripts for this process are in the directory
`old_NLP_stuff`.

Potentially userful scripts that are no longer used in the baseline project are in `oldstuff`.
