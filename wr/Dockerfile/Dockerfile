# docker run -it --rm \
#	-v $PWD:/sharedFolder \
#	--name ubuntu-gpp-1 \
#	ubuntu-gpp /bin/zsh

# docker run -p 8888:8888 --rm --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -it -v $PWD:/sharedFolder --name ubuntu-gpp-4  ubuntu-gpp /bin/zsh

# docker build -t ubuntu-gpp .

FROM ubuntu:18.04

RUN sed -i 's/archive.ubuntu.com/ftp.sjtu.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
vim \
zsh \
wget \
htop



RUN apt-get update && apt-get install -y \
python \ 
python-pip \ 
python3 \ 
python3-pip

RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

WORKDIR /root
