import numpy as np
"""
This is a simple script to use the HEFT function provided based on the example given in the original HEFT paper.
You have to define the DAG, compcost function and commcost funtion.

Each task/job is numbered 1 to 10
Each processor/agent is named 'a', 'b' and 'c'

Output expected:
Ranking:
[10, 8, 7, 9, 6, 5, 2, 4, 3, 1]
Schedule:
('a', [Event(job=2, start=27, end=40), Event(job=8, start=57, end=62)])
('b', [Event(job=4, start=18, end=26), Event(job=6, start=26, end=42), Event(job=9, start=56, end=68), Event(job=10, start=73, end=80)])
('c', [Event(job=1, start=0, end=9), Event(job=3, start=9, end=28), Event(job=5, start=28, end=38), Event(job=7, start=38, end=49)])
{1: 'c', 2: 'a', 3: 'c', 4: 'b', 5: 'c', 6: 'b', 7: 'c', 8: 'a', 9: 'b', 10: 'b'}
"""

verbose = False

dag = dict()
graph = np.zeros((1, 1))
communication_cpu = []
core = 0

def init_dag(g, cc, c):
    global communication_cpu, graph, core
    core = c
    graph = list(g)
    communication_cpu = list(cc)
    graph_to_dag(g)
    if verbose:
        print(dag)

def graph_to_dag(graph):
    global dag
    if verbose:
        print(graph)
    for u, x in enumerate(graph):
        dag[u+1] = set()
        for v, w in enumerate(x):
            if w == -1: continue
            dag[u+1].add(v+1)

def compcost(job, agent):
    if job == 0: return 0
    try:
        return communication_cpu[job - 1]
    except:
        print(len(dag), len(communication_cpu))
        return communication_cpu[job - 1]

def commcost(ni, nj, A, B):
    return 0

# for containerize
def commcost_con(ni, nj):
    global graph
    if ni == 0 or nj == 0: return 0
    return graph[ni-1][nj-1]