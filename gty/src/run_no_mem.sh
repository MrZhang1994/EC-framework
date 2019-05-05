#!/bin/bash
cnum=1000
for ((i=0; i<9; i++)) ; do
    for ((c=0; c<$cnum; c++)) ; do
        python main_no_mem.py -g 1 -n 1 -i $i -c $c
    done
done
