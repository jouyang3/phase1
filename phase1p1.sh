#!/bin/bash

mu=1
lambdas="0.1 0.23 0.4 0.55 0.65 0.8 0.9"
queue=9999999 # "infinite" queue size
outfile1="statsp1.csv"
outfile2="statsp1ec.csv"

rm -f "$outfile"
 
for lambda in $lambdas; do
	echo "Running with mu=$mu, queue=$queue, lambda=$lambda"
	./phase1.py $queue $mu $lambda "$outfile1" 0 > /dev/null
	./phase1.py $queue $mu $lambda "$outfile2" 1 > /dev/null
done
