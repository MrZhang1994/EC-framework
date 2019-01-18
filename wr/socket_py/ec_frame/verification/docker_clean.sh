sudo docker kill $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)