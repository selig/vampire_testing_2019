#! /bin/bash


python3 /home/leonardo/Project/TPTP-v7.2.0/test12.py
echo 'Bucketing Finished!';

while read line
do
	echo "STARTING NEW TEST" > result.txt
	echo "$line" >> result.txt
	$line>>result.txt
	python3 read2.py $line
	
done < /home/leonardo/Project/TPTP-v7.2.0/commands.txt

