# sudo docker run -p 8888:8888 --name mem_true_1 -itv ~/Desktop/zjw/gty/mem_true/src1:/home/jovyan/src1 jupyter/scipy-notebook
# sudo docker exec -it mem_true_1 /bin/bash
sudo docker start nb
out=`sudo docker exec nb jupyter notebook list`
echo $out | grep '^http' | sed 's/ .*//' | xargs xdg-open && sudo docker exec -it nb /bin/bash