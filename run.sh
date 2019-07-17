#! /bin/bash


python3 bucketting.py

while read line
do
	$line>>result.txt
	
done < commands.txt

python3 
