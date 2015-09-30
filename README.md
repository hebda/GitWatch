# GitWatch

GitWatch assigns a probability to a given repository stored on GitHub that the repository
contains a bug. This repository contains the scripts that are responsible for the construction
of the algorithm that assigns that probability.

### Step 1

Scrape data from the [GitHub Archive](githubarchive.org). This process is very slow.
* Create mySQL tables in the GitWatch database with:
** CREATE TABLE repo (id INT UNSIGNED, name TINYTEXT, private BOOL, created_at DATETIME, description TEXT, language TINYTEXT, watchers MEDIUMINT UNSIGNED);
** CREATE TABLE event (id INT UNSIGNED, type TINYINT UNSIGNED, timestamp DATETIME);
** CREATE INDEX id_index ON event (id); #This will improve performance a lot!
* runExtractor.sh downloads the json that contains all the events for a given hour.
** extractor.py processes the json and records the relevant information in the GitWatch mySQL db.
** extractor_csv.py outputs to file rather than SQL for running remotely. The results are moved to SQL locally with csv_to_{repo,event}_sql.py. Use sort <filename> | uniq -u to reduce the size of the repo.csv file!
* populateDB.py  populates the rest of the database info in SQL using GitHub API. The limit is 5k requests / hour with authentication.

### Step 2

Process the data and store in SQL
* makeDict.py looks at the first two weeks of data and outputs the 2000 most frequent words. Note that I went through the list by hand and removed the nonsense ones, e.g. single letters, 'fffffff', words in French and German
* repoCount.py counts the number of repos present in some time interval. This is needed in order to limit the training and testing set. Otherwise it will be too big.
* processData.py puts it all together. The output is a csv file for training, testing, and validation. The file combines event info and tf-vector.

### Step 3

Training
This was done with the iPython notebook in the training directory.
The 

### Step 4

Populate training to db. First create three new columns in the repo table.
* process_training.py creates a table of dimension n(repos) x 60 onto which training can be applied.
* populateDB_withpred.py fills in the values

### Step 5

Run the webapp
* run.py will run the web app on the local machine

## Check out gitwatch.xyz to see it run!
