#!/bin/sh
IMAGE="quoinedev/python3.6-pandas-alpine:latest"
n=10
iter=1000/n
# n=1
# iter=5/n

function run_docker {
	g=$1
	i=$2
	docker run -v $PWD:/home --rm --name jsc_$(expr $i + 1) $IMAGE python /home/main.py -g $g -i $i -n $n
}

for g in 1; do
	for i in {0..11}; do
		for((j=0;j<iter;j++)); do
			run_docker $g $i
			# echo run_docker $g $i
		done
	done
done