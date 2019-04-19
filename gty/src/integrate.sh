#!/bin/bash
cnum=20
cat df_heft00.csv | head -1 > df.csv
for ((c=0; c<$cnum; c++)) ; do
    for ((i=0; i<8; i++)) ; do
        sed -i '1d' df_heft$i$c.csv
        cat df_heft$i$c.csv >> df.csv
    done
done

rm df_*