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

df = pd.DataFrame(columns=('gid', 'core', 'Maximum memory'))

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

def main(gid):
    global df_cnt

    # init graph
    impact_factor, arc_num, vertex_num = maxcut.graph_parameter(gid)
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph(gid, vertex_num, arc_num, impact_factor)
    total_calculation_cost = sum(vertex_cpu)

    for core in [1, 2, 3, 4, 5, 6]:
        # calculate maxtopcut
        S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
        df.loc[df_cnt] = [gid, core, cut]
        df_cnt += 1

    return 0

if __name__ == '__main__':
    random.seed(datetime.now())

    # test numbers
    num = 100

    for gid in [1, 2, 3, 4]:
        records = 0
        while records < num:
            # if fail, ignore
            try:
                if main(gid) == 0:
                    records += 1
            except:
                continue
        print(gid)
    df.to_csv('./df_mem.csv', index = False)