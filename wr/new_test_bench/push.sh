rm -f verification/w*/*.log
rm -f verification/w*/local.file
rm -f verification/w2/*.zip
rm -f verification/w2/*.txt
rm -f verification/w2/*.output

cp verification/shared_lib.py verification/w1/shared_lib.py
cp verification/shared_lib.py verification/w2/shared_lib.py
cp verification/shared_lib.py verification/w3/shared_lib.py


rsync -azvh . wr@10.211.55.93:/home/wr/py_ipc --delete