## Build container

run `build_container.sh` to generate test/alpine image

## RUN

First run `ec_frame/verification/docker_clean.sh` to clean unneeded containers, this will stop and delete all containers on your machine.
Then run  `ec_frame/verification/docker_run.sh` to start


## scripts

`push.sh` transfer the local code to the virtual machine, will delete extra files at the destination

`pull.sh` pull all the files from the virtual machine to local, used to achieve log files

`ssh.sh` used to ssh to virtual machine and cd to proper dir.