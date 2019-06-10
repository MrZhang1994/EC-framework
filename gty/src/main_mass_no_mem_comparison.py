import sys
import getopt
import os
from datetime import datetime
import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag, verbose
from heft import heft
from cpop import cpop
from containerize import *
import draw

import pandas as pd
import numpy as np
from math import ceil
import time
import itertools

df = pd.DataFrame(columns=('Type', 'Total Pct.', 'Calculation Pct.', 'EDER', 'DOR', 'Time', 'Sched Time', 'gid', 'Case', 'Scheduling Algorithm'))

# parameters
cores = [2,    3,   4,    5,   6]
isol  = [1.5,  3,   5,  7.5, 10.5]

gg = [0, 12, 25, 41, 19, 11]
con = [3, 4, 5, 6, 7]

# index combinations
tests = [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1],   [2, 0], [2, 2], [2, 3], [2, 4]]

# record counter
df_cnt = 0

def get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, algo, Graph = graph):
    _ = time.time()
    cont, bridge_tasks, new_tasks = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, algo, Graph)
    cont_open = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan = new_tasks[vertex_num].aft
    return cont_open, makespan, sum([x.aft-x.ast for x in new_tasks]), time.time() - _

def main(k, gid):
    global df_cnt
    # get configuration
    core = cores[tests[k][0]]
    iso_limit = isol[tests[k][1]]

    # init graph
    impact_factor, arc_num, vertex_num = maxcut.graph_parameter(gid)
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph(gid, vertex_num, arc_num, impact_factor)
    total_calculation_cost = sum(vertex_cpu)
    
    # now we have a valid DAG

    # init example for heft
    # now the matrix 'graph', the dict 'dag', the matrix 'communication_cpu'
    # The index of 'dag' starts from 1
    example.init_dag(graph, communication_cpu, core)

    algo = ['HEFT', 'CPOP']
    for algo_index, schedule_algo in enumerate([heft, cpop]):
        # run heft
        # priority_list is a topological sequence of tasks in heft results, used to update containeration results
        _ = time.time()
        processors, tasks, priority_list = schedule_algo()
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

        # search_result = optimal(vertex_num, tasks, processors, dag, r_dag, order)
        # print(search_result)

        cont_open_f, makespan_f, busy_time_f, time_f = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'forward')
        cont_open_b, makespan_b, busy_time_b, time_b = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'backward')
        cont_open_i2c, makespan_i2c, busy_time_i2c, time_i2c = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'ICRB')
        cont_open_i, makespan_i, busy_time_i, time_i = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'STO')
        cont_open_r, makespan_r, busy_time_r, time_r = get_result(vertex_num, tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'rand')

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
        upper = one_tasks[vertex_num].aft

        open_upper = gg[gid]
        open_lower = ceil(gg[gid]/con[tests[k][1]])

        df.loc[df_cnt] = [
            'CPF',
            round(busy_time_fb / (makespan_fb*core), 4),
            round(total_calculation_cost / (makespan_fb*core), 4),
            # makespan_fb,
            round((makespan_fb - lower)/(upper - lower), 4),
            round((cont_open_fb - open_lower)/(open_upper - open_lower), 4),
            time_fb+time_heft, time_heft, gid, k, algo[algo_index]]
        df_cnt += 1

        df.loc[df_cnt] = [
            'ICRB',
            round(busy_time_i2c / (makespan_i2c*core), 4),
            round(total_calculation_cost / (makespan_i2c*core), 4),
            # makespan_i2c,
            round((makespan_i2c - lower)/(upper - lower), 4),
            round((cont_open_i2c - open_lower)/(open_upper - open_lower), 4),
            time_i2c+time_heft, time_heft, gid, k, algo[algo_index]]
        df_cnt += 1

        df.loc[df_cnt] = [
            'STO',
            round(busy_time_i / (makespan_i*core), 4),
            round(total_calculation_cost / (makespan_i*core), 4),
            # makespan_i,
            round((makespan_i - lower)/(upper - lower), 4),
            round((cont_open_i - open_lower)/(open_upper - open_lower), 4),
            time_i+time_heft, time_heft, gid, k, algo[algo_index]]
        df_cnt += 1


        df.loc[df_cnt] = [
            'Rand',
            round(busy_time_r / (makespan_r*core), 4),
            round(total_calculation_cost / (makespan_r*core), 4),
            # makespan_r,
            round((makespan_r - lower)/(upper - lower), 4),
            round((cont_open_r - open_lower)/(open_upper - open_lower), 4),
            time_r+time_heft, time_heft, gid, k, algo[algo_index]]
        df_cnt += 1

    return 0

if __name__ == '__main__':
    random.seed(datetime.now())

    # test numbers
    num = 1000

    for gid in [5]:
       for k in [1]:
            records = 0
            while records < num:
                # if fail, ignore
                """
                try:
                    if main(k, gid) == 0:
                        records += 1
                except:
                    continue
                """
                main(k, gid)
                records += 1
            print(gid, k)
    df.to_csv('./df_mass.csv', index = False)
