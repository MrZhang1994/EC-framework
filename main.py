import sys
import getopt
import os
from datetime import datetime
import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag, verbose
from ic_pcp import ic_pcp
from cpop import cpop
from heft import heft
from moheft import moheft
from dls import dls
from hlfet import hlfet
from containerize import *
import draw

import pandas as pd
import numpy as np
from math import ceil
import time
import itertools

import logging
logging.basicConfig(level=logging.INFO)

df_EDR = pd.DataFrame(columns=('max','min','CPF','ICRO','STO','Rand'))
df_DOR = pd.DataFrame(columns=('max','min','CPF','ICRO','STO','Rand'))
df_COM = pd.DataFrame(columns=('max','CPF','ICRO','STO','Rand'))
df_ALG = pd.DataFrame(columns=('SCHED', 'CPF','ICRO','STO','Rand'))

# parameters
cores = [2, 3, 4, 5, 6]
isol  = [1, 3, 5, 7, 9]
# isol  = [1.5, 3, 5, 7.5, 10.5]

gg = [0, 11, 25, 41, 19, 8, 11, 16]
con = [2, 4, 5, 6, 6]
# con = [3, 4, 5, 6, 7]

# index combinations
tests = [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [1, 0], [1, 2], [1, 3], [1, 4]]
# case 1: core = 2, iso = 3
# case 2: core = 3, iso = 3
# case 3: core = 4, iso = 3
# case 4: core = 5, iso = 3
# case 5: core = 6, iso = 3
# case 6: core = 3, iso = 1.5
# case 7: core = 3, iso = 5
# case 8: core = 3, iso = 7.5
# case 9: core = 3, iso = 10.5

# record counter
df_cnt = 0

def get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, algo, Graph = graph):
    _ = time.time()
    cont, bridge_tasks, new_tasks, bridge_com = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, algo, Graph)
    cont_open = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan = new_tasks[vertex_num].aft
    return cont_open, makespan, time.time() - _, bridge_com

def main(k, gid):
    global df_cnt
    # get configuration
    core = cores[tests[k][0]]
    iso_limit = isol[tests[k][1]]

    # init graph
    impact_factor, arc_num, vertex_num = maxcut.graph_parameter(gid)
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph(gid, vertex_num, arc_num, impact_factor)

    # calculate maxtopcut
    # S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    # calculate the required memory constraints

    # now we have a valid DAG

    # init example for heft
    # now the matrix 'graph', the dict 'dag', the matrix 'communication_cpu'
    # The index of 'dag' starts from 1
    example.init_dag(graph, communication_cpu, core)

    # run heft
    # priority_list is a topological sequence of tasks in heft results, used to update containeration results
    _ = time.time()
    processors, tasks, priority_list = schedule_func()
    time_heft = time.time() - _

    # extract the task id from priority_list
    order = [t.id for t in priority_list]

    
    # 'dag_d' is 'dag' with core dependency
    # 'r_dag' is the reversed dag
    # It also calculates the influence index
    # t is the id of last task, starting from 1
    # N is the number of tasks starting from 1, but included 0.
    # Basically N = t + 1
    # Different index causes this mess orz
    _ = time.time()
    dag_d, r_dag, index, t, N, cpath = containerize_init(dag, tasks, processors, iso_limit, graph)
    time_fb = time.time() - _


    # lower bound of containerization is the finish time of the last task
    lower = tasks[vertex_num].aft
    if False:
        _ = time.time()
        search_EDER_SFE, search_DOR_SFE, com_SFE, search_EDER_SFD, search_DOR_SFD, com_SFD, search_EDER_SFC, search_DOR_SFC, com_SFC = optimal(vertex_num, tasks, processors, dag, r_dag, order)
        time_o = time.time() - _

    cont_open_f, makespan_f, time_f, com_f = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'forward')
    cont_open_b, makespan_b, time_b, com_b = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'backward')
    cont_open_i2c, makespan_i2c, time_i2c, com_i2c = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'ICRB')
    cont_open_i, makespan_i, time_i, com_i = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'STO')
    cont_open_r, makespan_r, time_r, com_r = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'rand')
    
    if makespan_f < makespan_b:
        makespan_fb, cont_open_fb, time_fb, com_fb = makespan_f, cont_open_f, time_f + time_fb, com_f
    else:
        makespan_fb, cont_open_fb, time_fb, com_fb = makespan_b, cont_open_b, time_b + time_fb, com_b

    # upper bound
    cont = dict()
    for i in range(vertex_num+1):
        cont[i] = set()
        cont[i].add(i)
    one_tasks, com_max = update_schedule(dag, r_dag, processors, tasks, range(1, vertex_num + 1), order, [i for i in range(vertex_num + 1)])
    upper = one_tasks[vertex_num].aft
    
    open_upper = gg[gid]
    open_lower = min([ceil(gg[gid]/con[tests[k][1]]), cont_open_fb, cont_open_i2c, cont_open_i, cont_open_r])

    if False:
        # make sure SFE and SFE are the lowest
        if search_EDER_SFE > makespan_fb:
            search_EDER_SFE = makespan_fb
            search_DOR_SFE = cont_open_fb
            com_SFE = com_fb

        if search_EDER_SFE > makespan_i2c:
            search_EDER_SFE = makespan_i2c
            search_DOR_SFE = cont_open_i2c
            com_SFE = com_i2c

        if search_EDER_SFE > makespan_i:
            search_EDER_SFE = makespan_i
            search_DOR_SFE = cont_open_i
            com_SFE = com_i

        if search_EDER_SFE > makespan_r:
            search_EDER_SFE = makespan_r
            search_DOR_SFE = cont_open_r
            com_SFE = com_r

        # DOR
        if search_DOR_SFD > cont_open_fb:
            search_EDER_SFD = makespan_fb
            search_DOR_SFD = cont_open_fb
            com_SFD = com_fb

        if search_DOR_SFD > cont_open_i2c:
            search_EDER_SFD = makespan_i2c
            search_DOR_SFD = cont_open_i2c
            com_SFD = com_i2c

        if search_DOR_SFD > cont_open_i:
            search_EDER_SFD = makespan_i
            search_DOR_SFD = cont_open_i
            com_SFD = com_i

        if search_DOR_SFD > cont_open_r:
            search_EDER_SFD = makespan_r
            search_DOR_SFD = cont_open_r
            com_SFD = com_r
        
        if com_SFC > com_fb:
            search_EDER_SFC = makespan_fb
            search_DOR_SFC = cont_open_fb
            com_SFC = com_fb
        
        if com_SFC > com_i2c:
            search_EDER_SFC = makespan_i2c
            search_DOR_SFC = cont_open_i2c
            com_SFC = com_i2c
        
        if com_SFC > com_i:
            search_EDER_SFC = makespan_i
            search_DOR_SFC = cont_open_i
            com_SFC = com_i

        if com_SFC > com_r:
            search_EDER_SFC = makespan_r
            search_DOR_SFC = cont_open_r
            com_SFC = com_r

    EDR = [
        round(upper, 4), # max
        round(lower, 4), # min
        round(makespan_fb, 4), # CPF
        round(makespan_i2c, 4), # ICRO
        round(makespan_i, 4), # STO
        round(makespan_r, 4)]

    DOR = [
        round(open_upper, 4), # max
        round(open_lower, 4), # min
        round(cont_open_fb, 4),
        round(cont_open_i2c, 4),
        round(cont_open_i, 4),
        round(cont_open_r, 4)]

    COM = [
        round(com_max, 4),
        round(com_fb, 4),
        round(com_i2c, 4),
        round(com_i, 4),
        round(com_r, 4)]
    
    ALG = [
        round(time_heft, 4), # heft
        round(time_fb+time_heft, 4), # CPF
        round(time_i2c+time_heft, 4), # ICRO
        round(time_i+time_heft, 4), # STO
        round(time_r+time_heft, 4)]

    if False:
        EDR.append(round(search_EDER_SFE, 4))
        EDR.append(round(search_EDER_SFD, 4))
        EDR.append(round(search_EDER_SFC, 4))
        DOR.append(round(search_DOR_SFE, 4))
        DOR.append(round(search_DOR_SFD, 4))
        DOR.append(round(search_DOR_SFC, 4))
        COM.append(round(com_SFE, 4))
        COM.append(round(com_SFD, 4))
        COM.append(round(com_SFC, 4))
        ALG.append(round(time_o/3+time_heft, 4)) # SFE, SFD, SFC
        ALG.append(round(time_o/3+time_heft, 4)) # SFE, SFD, SFC

    df_EDR.loc[df_cnt] = EDR
    df_DOR.loc[df_cnt] = DOR
    df_COM.loc[df_cnt] = COM
    df_ALG.loc[df_cnt] = ALG

    df_cnt += 1
    return 0

def appendDF(fname, df):
    fname = algo_name + '/' + fname
    if not os.path.isfile(fname):
        df.to_csv(fname, header='column_names', index=False)
    else:
        df.to_csv(fname, mode='a', header=False, index=False)

if __name__ == '__main__':
    random.seed(datetime.now())

    # test numbers
    algo = {'heft': heft, 'cpop': cpop, 'ic_pcp': ic_pcp, 'dls': dls, 'hlfet': hlfet, 'moheft': moheft}
    num = 1000
    case_graph = 1
    case_index = 1
    algo_name = 'moheft'
    schedule_func = algo[algo_name]
    # opts
    opts, args = getopt.getopt(sys.argv[1:], 'vs:g:i:n:')
    for o, a in opts:
        if o in ('-v', '--verbose'):
            verbose = True
        elif o in ('-s', '--sched'):
            schedule_func = algo[a]
            algo_name = a
        elif o in ('-g', '--graph'):
            case_graph = int(a)
            # if case_graph == 5:
            #     df_EDR = pd.DataFrame(columns=('max','min','CPF','ICRO','STO','Rand','SFE','SFD','SFC'))
            #     df_DOR = pd.DataFrame(columns=('max','min','CPF','ICRO','STO','Rand','SFE','SFD','SFC'))
            #     df_COM = pd.DataFrame(columns=('max','CPF','ICRO','STO','Rand','SFE','SFD','SFC'))
            #     df_ALG = pd.DataFrame(columns=(algo_name, 'CPF','ICRO','STO','Rand','SFE','SFD'))
        elif o in ('-i', '--index'):
            case_index = int(a)
        elif o in ('-n', '--number'):
            num = int(a)
        else:
            sys.exit()

    for gid in [case_graph]:
        for k in [case_index]:
            records = 0
            while records < num:
                # if fail, ignore
                try:
                    if main(k, gid) == 0:
                        records += 1
                        print(records)
                except:
                    continue

    appendDF('{}_NED_{}_{}.csv'.format(algo_name, case_graph, case_index+1), df_EDR)
    appendDF('{}_DOR_{}_{}.csv'.format(algo_name, case_graph, case_index+1), df_DOR)
    appendDF('{}_ICP_{}_{}.csv'.format(algo_name, case_graph, case_index+1), df_COM)
    appendDF('{}_TIME_{}_{}.csv'.format(algo_name, case_graph, case_index+1), df_ALG)
    # os.system('ls /home')