rm -f verification*/w*/*.log
rm -f verification*/w*/local.file
rm -f verification*/w*/*.output

rm -f verification*/w2/*.zip
rm -f verification*/w2/*.txt
rm -f verification*/w2/*.output
rm -rf verification*/w2/images_to_send

rm -f verification*/w3/*.txt
rm -rf verification*/w3/test_images
rm -rf verification*/w3/images_to_send

rm -rf verification*/w*/__*
rm -rf verification*/w*/.keras

rm -rf verification*/w*/start.time*
rm -rf verification*/w*/test*/start.time*


cp verification/shared_lib.py verification/w1/shared_lib.py
cp verification/shared_lib.py verification/w2/shared_lib.py
cp verification/shared_lib.py verification/w3/shared_lib.py

cp verification2/shared_lib.py verification2/w2/shared_lib.py
cp verification2/shared_lib.py verification2/w3/shared_lib.py
cp verification2/shared_lib.py verification2/w4/shared_lib.py


# parallel virtual machine
#rsync -azvh . wr@10.211.55.94:/home/wr/py_ipc --delete

# wanglab 2 core old machine
#rsync -azvh -p 60001 zjw@192.168.0.100/home/zjw/py_ipc/  .
#rsync -azvh -e 'ssh -p 60001' . zjw@192.168.0.100:/home/zjw/py_ipc  --delete

# wanglab big machine
rsync -azvh -e 'ssh -p 8098' . wanglab@192.168.0.9:/home/wanglab/Desktop/zjw/py_ipc  --delete

# wanglab 
# ssh -t wanglab@192.168.0.9 -p 8098 "cd /home/wanglab/Desktop/zjw ; bash"

# wanglab pi3
#rsync -azvh -e 'ssh -p 22' . pi@192.168.0.112:/home/pi/py_ipc  --delete