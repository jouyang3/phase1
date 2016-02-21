#!/bin/bash

mu=1
lambdas="0.1 0.23 0.4 0.55 0.65 0.8 0.9"
queue=9999999 # "infinite" queue size

rm -f stat.csv

for lambda in $lambdas; do
	echo "Running with mu=$mu, queue=$queue, lambda=$lambda"
	"./$1" $queue $mu $lambda
done
