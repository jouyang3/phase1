#!/bin/bash

mu=1
lambdas="0.2 0.4 0.6 0.8 0.9"
queues="1 20 50"

output1=statsp3.csv
output2=statsp3ec.csv

for queue in $queues; do
	for lambda in $lambdas; do
		echo "Running with mu=$mu, queue=$queue, lambda=$lambda"
		./phase1.py $queue $mu $lambda $output1 0 > /dev/null
		./phase1.py $queue $mu $lambda $output2 1 > /dev/null
	done
done
