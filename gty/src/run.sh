#!/bin/bash
cnum=20
for ((c=0; c<$cnum; c++)) ; do
    for ((i=0; i<14; i++)) ; do
        python main.py -g 1 -n 5 -i $i -c $c
    done
done