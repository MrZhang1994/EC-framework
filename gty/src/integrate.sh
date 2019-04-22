#!/bin/bash
cnum=100
cat df_heft0_0.csv | head -1 > df.csv
for ((c=0; c<$cnum; c++)) ; do
    for ((i=0; i<8; i++)) ; do
        sed -i '1d' df_heft$i\_$c.csv
        cat df_heft$i\_$c.csv >> df.csv
    done
done

rm df_*