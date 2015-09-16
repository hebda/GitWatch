#!/bin/bash

year=2015
maxindex=7
month=(01 02 03 04 05 06 07 08 09)
maxday=(31 28 31 30 31 30 31 31 12)

for i in `seq 0 $maxindex`
do
    for j in `seq 1 ${maxday[$i]}`
    do
	if [ $j -lt 10 ]
	then
	    date=$year-${month[$i]}-0$j
	else
	    date=$year-${month[$i]}-$j
	fi
	for k in {0..23}
	do
	    datehr=$date-$k
	    filename=${datehr}.json
	    
	    #check if the file was already processed.
	    teststr=`grep $filename -lir done.txt`
	    if [ "$teststr" == "done.txt" ]
	    then
		continue
	    fi
	    
	    wget http://data.githubarchive.org/${filename}.gz
	    gunzip ${filename}.gz
	    ./extractor.py $filename
	    rm $filename
	    echo $filename >> done.txt
	done
    done
done

