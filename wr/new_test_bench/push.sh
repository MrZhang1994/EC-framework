rm -f verification/w*/*.log
rsync -azvh . wr@10.211.55.93:/home/wr/py_ipc --delete