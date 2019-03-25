import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag, verbose
from heft import heft
from containerize import *
import draw
import os
import pandas as pd

cores = [100, 1,  2,    3,   4,    5,   6, 7, 8, 9, 10]

def main(gid):

    df = pd.DataFrame(columns=('Unlimited', 'core 1', 'core 2', 'core 3', 'core 4', 'core 5', 'core 6', 'core 7', 'core 8', 'core 9', 'core 10'))
    cnt = 0
    # path = './results_heft/graph' + str(gid) + '/' + str(k) + '/'

    # init graph
    for i in range(100):
        total = []
        ratio = []
        impact_factor, arc_num, vertex_num = maxcut.graph_parameter(gid)
        graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph(gid, vertex_num, arc_num, impact_factor)

        # calculate maxtopcut
        for k in range(11):
            S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, cores[k])
            total.append(cut)
            ratio.append(float(total[k] / total[0]))
            
        df.loc[cnt] = ratio 
        cnt += 1 

    ls = df.mean()
    print(ls)
    
    return 0

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        os.system('rm -rf ' + path + '/*')

if __name__ == '__main__':
    print('Graph 1: \n')
    gid = 1
    main(gid)
    print('Graph 2: \n')
    gid = 2
    main(gid)
    print('Graph 3: \n')
    gid = 3
    main(gid)
    print('Graph 4: \n')
    gid = 4
    main(gid)
    """
    num = 1000
    create_dir('./results_heft')
    for gid in [1, 2, 3, 4]:
        create_dir('./results_heft/graph' + str(gid))
        for k in range(1000):
            create_dir('./results_heft/graph' + str(gid) + '/' + str(k))
            cnt = 0
            while cnt < num:
                try:
                    if main(k, gid) == 0:
                        cnt += 1
                except:
                    continue
    """
