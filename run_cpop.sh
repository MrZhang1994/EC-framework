#!/bin/sh
IMAGE="quoinedev/python3.6-pandas-alpine:latest"
if [ "$1" = "test" ]; then
	n=1
	iter=2/n
	echo testing
else
	n=10
	iter=1000/n
fi

function run_docker {
	g=$1
	i=$2
	docker run -v $PWD:/home --rm --name jsc5_cpop_$(expr $i + 1) $IMAGE python /home/main.py -c -g $g -i $i -n $n
}

for g in 5; do
	for i in {0..8}; do
		for((j=0;j<iter;j++)); do
			run_docker $g $i
		done
	done
done