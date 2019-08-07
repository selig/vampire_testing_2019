#! /bin/bash


python3 /Users/leo/Documents/leovampire/SMT/test11.py
echo 'Bucketing Finished!';

counter = 0
while read lin
do
	now = $(date + "%T")	
	echo "Running test $counter at $now"
	echo "STARTING NEW TEST" > result.txt
	echo "$line" >> result.txt
	gtimeout 11 $line >> result.txt
	python3 collect_results_SMT.py $line
	#arr1 = $ ($line)
	#arr2 = $ (echo$ {arr1[1]} | tr "/" "\n")
	#arr3 = $ ($arr2)
	#problem = $ {arr3[9]}
	#strat = $ {arr1[5]}
	#mv result.txt "tmp/${problem}_${strat}"
	counter = $((counter+1)
	
done < commands.txt

