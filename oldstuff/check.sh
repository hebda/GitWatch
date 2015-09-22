#!/bin/bash

empty=(`ls tmpjson*`)

for i in "${empty[@]}"
do
    filename=${i}
    repoid=${filename:8}
    if [ `cat $filename | wc -c` == "0" ]
    then
	wget -O repo_info/$filename https://api.github.com/repositories/${repoid}\?access_token=86e4b6b7e573c30543a27243e7459c04d6683c80
	if [ `cat repo_info/$filename | wc -c` == "0" ]
	then
	    echo "Deleted $filename" >> private.txt
	    rm repo_info/$filename
	fi
	rm $filename
    fi
done
