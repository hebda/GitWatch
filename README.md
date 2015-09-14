# GitWatch

GitWatch assigns a probability to a given repository stored on GitHub that the repository
contains a bug.
This repository contains the scripts that are responsible for the construction of the 
algorithm that assigns that probability.

### Step 1

Scrape data from the [GitHub Archive](githubarchive.org).

runExtractor.sh downloads the json that contains all the events for a given hour.
extractor.py processes the json and records the relevant information in text.csv and events.csv.
This process is very slow.

### Step 2

Process the data and store in SQL


### Step 3
Training

