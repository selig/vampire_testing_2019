#! /bin/bash


python3 /Users/leo/Documents/leovampire/SMT/test11.py

echo 'Bucketing Finished!';

counter=0
while read line
do
	now=$(date +"%T")
	echo "Running test $counter at $now"
	echo "STARTING NEW TEST" > result_SMT.txt
	echo "$line" >> result_SMT.txt
	gtimeout 11 $line>>result_SMT.txt
	python3 collect_results.py $line
	#arr1=$( $line )
	#arr2=$( echo ${arr1[1]} | tr "/" "\n" )
	#arr3=$( $arr2 )
	#problem=${arr3[9]}
	#strat=${arr1[5]}
	#mv result.txt "tmp/${problem}_${strat}"
	counter=$((counter+1))
	
done < commands_SMT.txt

echo 'Collection finished!'
