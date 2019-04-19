import matplotlib.pyplot as plt


def read_and_print(input_file_dir, output_file_dir, mode):
    f = open(input_file_dir, "r")
    array1 = []
    i = 0
    for line in f:
        lx = line
        array1.append(float(lx[1:-1]))
        i = i+1
        # if i > 500:
        #   break
    # print(array1)
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


#read_and_print("log/log", "a.png", "not")
#read_and_print("../tools/procstat/docker_cd_s.log", "b.png", 'diff')
#read_and_print("../tools/procstat/dockerd_u.log", "c.png", 'diff')
#read_and_print("../tools/procstat/dockerd_s.log", "d.png", 'diff')

read_and_print("log/dockerd.log", "fig/dd.png", "not")
read_and_print("log/dockerd.log", "fig/ddd.png", "diff")


#read_and_print("../tools/procstat/dockerd_s.log", "d.png", 'diff')
