# ECB
Edge computing bench

# Reviewed version
Do a specific work.
DONE: transmit file between containers, the ways is to use `--net=host`


## TODO:

###  p1
t1-work -> t1-send + t2-rec -> t2-work 

### p2
run in  "docker in docker"

### p3
run based on scheduled graph

## Resources

### docker in docker (embedded docker )
https://github.com/jpetazzo/dind 

### ipc in linux 
Overview
http://man7.org/conf/lca2013/IPC_Overview-LCA-2013-printable.pdf

FIFO 
https://linux.die.net/man/7/fifo


### posix in c

https://www.softprayog.in/programming/interprocess-communication-using-fifos-in-linux

### send file via socket in python 
https://stackoverflow.com/questions/9382045/send-a-file-through-sockets-in-python

### Quickly create a large file on a Linux system
https://stackoverflow.com/questions/257844/quickly-create-a-large-file-on-a-linux-system
