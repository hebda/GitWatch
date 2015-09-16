# GitWatch

GitWatch assigns a probability to a given repository stored on GitHub that the repository
contains a bug. This repository contains the scripts that are responsible for the construction
of the algorithm that assigns that probability.

### Step 1

Scrape data from the [GitHub Archive](githubarchive.org). This process is very slow.
* runExtractor.sh downloads the json that contains all the events for a given hour.
* extractor.py processes the json and records the relevant information in text.csv and events.csv.

### Step 2

Process the data and store in SQL
* makeDict.py looks at the first two weeks of data and outputs the 2000 most frequent words. Note that I went through the list by hand and removed the nonsense ones, e.g. single letters, 'fffffff', words in French and German
* processData.py puts it all together. The output is a csv file for training, testing, and validation. The file combines event info and tf-vector.

### Step 3

Training

