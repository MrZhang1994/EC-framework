for ((c=0; c<5; c++)) ; do
    for ((i=0; i<8; i++)) ; do
        python main.py -g 1 -n 5 -i $i -c $c
    done
done