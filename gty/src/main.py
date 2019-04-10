import sys
import getopt
import os
from datetime import datetime
import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag, verbose
from heft import heft
from containerize import *
import draw

import pandas as pd
import numpy as np
from math import ceil
import time
import itertools

df = pd.DataFrame(columns=('Type', 'Total Pct.', 'Calculation Pct.', 'EDER', 'DOR', 'Time', 'Heft Time', 'gid', 'Case', 'Lower Bound', 'Upper Bound'))

# parameters
cores = [2,    3,   4,    5,   6]
mem   = [1, 0.95, 0.9, 0.85,  0.8, 0.75]
isol  = [1.5,  3,   5,  7.5, 10.5]

gg = [0, 12, 25, 41, 19]
con = [3, 4, 5, 6, 7]

# index combinations
tests = [[0, 2, 1], [1, 2, 1], [2, 2, 1], [3, 2, 1], [4, 2, 1], [2, 0, 1], [2, 1, 1], [2, 3, 1], [2, 4, 1], [2, 5, 1], [2, 2, 0], [2, 2, 2], [2, 2, 3], [2, 2, 4]]

# record counter
df_cnt = 0

def get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, algo, Graph = graph):
    _ = time.time()
    cont, bridge_tasks, new_tasks = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, algo, Graph)
    if verbose:
        print(algo + ':')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, algo + '.png')
        print(new_tasks[vertex_num].aft)
        print(cont)
    cont_open = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan = new_tasks[vertex_num].aft
    return cont_open, makespan, sum([x.aft-x.ast for x in new_tasks]), time.time() - _

def main(k, gid):
    global df_cnt
    # get configuration
    core = cores[tests[k][0]]
    Mem = mem[tests[k][1]]
    iso_limit = isol[tests[k][2]]

    # init graph
    impact_factor, arc_num, vertex_num = maxcut.graph_parameter(gid)
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph(gid, vertex_num, arc_num, impact_factor)
    total_calculation_cost = sum(vertex_cpu)

    # calculate maxtopcut
    S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    # calculate the required memory constraints
    M = cut * Mem

    # calculate backward edge
    init_minLevel(vertex_num, graph)
    tmpu = 0
    tmpv = 0
    while cut > M:
        if verbose:
            print(S, T)
        # Use heuristic to get new edge
        u, v = minLevel(graph, S, T, 0, vertex_num-1)
        # no valid edge or unknown problem (new edge was just added, nobody knows why)
        if (u == 0 and v == 0) or (tmpu == u and tmpv == v):
            if verbose:
                print('MinLevel Heuristic Failed\n')
            return -1
        tmpu = u
        tmpv = v
        # add new edge to graph
        maxcut.update_graph(graph, u, v)
        # calculate maxtopcut again
        S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    
    # now we have a valid DAG

    # init example for heft
    # now the matrix 'graph', the dict 'dag', the matrix 'communication_cpu'
    # The index of 'dag' starts from 1
    example.init_dag(graph, communication_cpu, core)

    # run heft
    # priority_list is a topological sequence of tasks in heft results, used to update containeration results
    _ = time.time()
    processors, tasks, priority_list = heft()
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

    search_result = optimal(vertex_num, tasks, processors, dag, r_dag, order)
    print(search_result)

    cont_open_f, makespan_f, busy_time_f, time_f = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'forward')
    cont_open_b, makespan_b, busy_time_b, time_b = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'backward')
    cont_open_i2c, makespan_i2c, busy_time_i2c, time_i2c = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'ICRB')
    cont_open_i, makespan_i, busy_time_i, time_i = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'STO')
    cont_open_r, makespan_r, busy_time_r, time_r = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'rand')

    """
    Graph = [[i if (i != -1) else 0 for i in x ] for x in graph]
    Graph = Graph + np.transpose(Graph)
    cont_open_sc, makespan_sc, busy_time_sc, time_sc = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'sc', Graph)
    """
    
    if makespan_f < makespan_b:
        makespan_fb, cont_open_fb, busy_time_fb, time_fb = makespan_f, cont_open_f, busy_time_f, time_f + time_fb
    else:
        makespan_fb, cont_open_fb, busy_time_fb, time_fb = makespan_b, cont_open_b, busy_time_b, time_b + time_fb

    # upper bound
    cont = dict()
    for i in range(vertex_num+1):
        cont[i] = set()
        cont[i].add(i)
    one_tasks = update_schedule(dag, r_dag, processors, tasks, range(1, vertex_num + 1), order, [i for i in range(vertex_num + 1)])
    if verbose:
        print('upper bound:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in one_tasks], cont, 'upper.png')
        print(one_tasks[vertex_num].aft)
        print(cont)
    upper = one_tasks[vertex_num].aft

    if verbose:
        print('-'*10)
        print('lower: ')
        print(lower)
        print('upper: ')
        print(upper)
        print('CDF: ')
        print(makespan_fb)
        # print(round((makespan_fb - lower)/(upper - lower), 4))
        print('ICRB: ')
        print(makespan_i2c)
        # print(round((makespan_i2c - lower)/(upper - lower), 4))
        print('STO: ')
        print(makespan_i)
        # print(round((makespan_i - lower)/(upper - lower), 4))
        # print('sc: ')
        # print(round((makespan_s - lower)/(upper - lower), 4))
        print('random: ')
        print(makespan_r)
        # print(round((makespan_r - lower)/(upper - lower), 4))
    
    open_upper = gg[gid]
    open_lower = ceil(gg[gid]/con[tests[k][2]])

    df.loc[df_cnt] = [
        'CPF',
        round(busy_time_fb / (makespan_fb*core), 4),
        round(total_calculation_cost / (makespan_fb*core), 4),
        # makespan_fb,
        round((makespan_fb - lower)/(upper - lower), 4),
        round((cont_open_fb - open_lower)/(open_upper - open_lower), 4),
        time_fb+time_heft, time_heft, gid, k,
        lower, upper]
    df_cnt += 1

    df.loc[df_cnt] = [
        'ICRB',
        round(busy_time_i2c / (makespan_i2c*core), 4),
        round(total_calculation_cost / (makespan_i2c*core), 4),
        # makespan_i2c,
        round((makespan_i2c - lower)/(upper - lower), 4),
        round((cont_open_i2c - open_lower)/(open_upper - open_lower), 4),
        time_i2c+time_heft, time_heft, gid, k,
        lower, upper]
    df_cnt += 1

    df.loc[df_cnt] = [
        'STO',
        round(busy_time_i / (makespan_i*core), 4),
        round(total_calculation_cost / (makespan_i*core), 4),
        # makespan_i,
        round((makespan_i - lower)/(upper - lower), 4),
        round((cont_open_i - open_lower)/(open_upper - open_lower), 4),
        time_i+time_heft, time_heft, gid, k,
        lower, upper]
    df_cnt += 1

    
    df.loc[df_cnt] = [
        'Rand',
        round(busy_time_r / (makespan_r*core), 4),
        round(total_calculation_cost / (makespan_r*core), 4),
        # makespan_r,
        round((makespan_r - lower)/(upper - lower), 4),
        round((cont_open_r - open_lower)/(open_upper - open_lower), 4),
        time_r+time_heft, time_heft, gid, k,
        lower, upper]
    df_cnt += 1

    df.loc[df_cnt] = [
        'DFS',
        0,
        0,
        round((search_result - lower)/(upper - lower), 4),
        0,
        0, 0, gid, k,
        lower, upper]
    df_cnt += 1
    
    """
    df.loc[df_cnt] = [
        'SC',
        round(busy_time_sc / (makespan_sc*core), 4),
        round(total_calculation_cost / (makespan_sc*core), 4),
        round((makespan_sc - lower)/(upper - lower), 4),
        round((cont_open_sc - open_lower)/(open_upper - open_lower), 4),
        time_sc+time_heft, time_heft, gid, k,
        lower, upper]
    df_cnt += 1
    """

    return 0

if __name__ == '__main__':
    random.seed(datetime.now())

    # test numbers
    num = 15
    case_graph = 1
    case_indices = range(8)
    # opts
    opts, args = getopt.getopt(sys.argv[1:], 'vg:i:n:')
    for o, a in opts:
        if o in ('-v', '--verbose'):
            verbose = True
        elif o in ('-g', '--graph'):
            case_graph = int(a)
        elif o in ('-i', '--index'):
            case_indices = [int(a)]
        elif o in ('-n', '--number'):
            num = int(a)
        else:
            sys.exit()

    if verbose:
        main(case_graph, case_index)
        sys.exit()

    # for gid in [1, 2, 3, 4]:
    #    for k in range(len(tests)):
    for gid in [case_graph]:
        for k in case_indices:
            records = 0
            while records < num:
                # if fail, ignore
                try:
                    if main(k, gid) == 0:
                        records += 1
                except:
                    continue
            print(gid, k)
    df.to_csv('./df_heft.csv', index = False)