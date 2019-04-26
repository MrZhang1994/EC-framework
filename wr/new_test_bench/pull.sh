# parallel virtual machine
#rsync -azvh  wr@10.211.55.94:/home/wr/py_ipc/ .

#rsync -azvh -p 60001 zjw@202.121.180.26:/home/zjw/py_ipc/  .

# wanglab 2 core old machine
#rsync -azvh -p 60001 zjw@192.168.0.100:/home/zjw/py_ipc/  .

# wanglab big machine
#rsync -azvh -e 'ssh -p 8098' . zjw@192.168.0.9:/home/wanglab/Desktop/zjw/py_ipc  --delete

# wanglab pi3
rsync -azvh -p 22 pi@192.168.0.112:/home/pi/py_ipc/  .