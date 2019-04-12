#!/bin/bash
cnum=1
for ((c=0; c<$cnum; c++)) ; do
    for ((i=0; i<8; i++)) ; do
        python main.py -g 1 -n 1 -i $i -c $c
    done
done