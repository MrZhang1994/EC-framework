# sudo docker run -p 8888:8888 --name nb -itv /home/timmy/Documents/EC-framework/gty/src:/home/jovyan/src jupyter/scipy-notebook
sudo docker start nb
out=`sudo docker exec nb jupyter notebook list`
echo $out | grep '^http' | sed 's/ .*//' | xargs xdg-open && sudo docker exec -it nb /bin/bash