#! /bin/bash


python3 /home/leonardo/Project/SMT/test11.py
echo 'Bucketing Finished!';

while read line
do
	echo "STARTING NEW TEST" > result.txt
	echo "$line" >> result.txt
	$line>>result.txt
	python3 read2.py $line
	
done < /home/leonardo/Project/SMT/commands.txt

