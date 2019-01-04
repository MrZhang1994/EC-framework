import threading
#import matplotlib.pyplot as plt
import os

def printit():
	threading.Timer(0.1, printit).start()
	os.system(" ./psu 865 >> log/dockerd.log")
	os.system(" ./psu 876 >> log/docker_containerd.log")

"""
def read_and_print(input_file_dir, output_file_dir, mode):
    f = open(input_file_dir, "r")
    array1 = []
    i = 0
    for line in f:
        lx = line
        array1.append(float(lx[1:-1]))
        i = i+1
        if i > 500:
            break
    array2 = array1[1:-2]
    array3 = array1[2:-1]
    array4 = []
    for i in range(len(array2)):
        array4.append(array3[i]-array2[i])
    fig, ax = plt.subplots(nrows=1, ncols=1)
    if mode == "diff":
        ax.plot(array4)
    else:
        ax.plot(array1)
    fig.savefig(output_file_dir)   # save the figure to file
    plt.close(fig)



def draw_all():
	read_and_print("log/dockerd.log", "dd.png", "not")
	read_and_print("log/docker_containerd.log", "dcd.png", "not")
	read_and_print("log/dockerd.log", "ddd.png", "diff")
	read_and_print("log/docker_containerd.log", "dcdd.png", "diff")
	#  dcd stands for Docker ContainerD overall graph
	#
	#  dcdd stands for Docker ContainerD Diff graph, 
	#  which is the derivative of dcd
"""

def my_setup():
	os.system("rm -rf log")
	os.system("mkdir log")
	os.system("rm -rf fig")
	os.system("mkdir fig")



my_setup()
printit()
#draw_all()
