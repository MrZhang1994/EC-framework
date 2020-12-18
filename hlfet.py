import example
from example import dag, commcost, compcost
import statistics as stats
from decimal import Decimal, ROUND_DOWN
import logging
import numpy as np
import copy
import random
from operator import itemgetter

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(level=logging.INFO)


# Set the computation costs of tasks and communication costs of edges with mean values.
# Compute rank_u for all tasks by traversing graph upward, starting from the exit task.
# Sort the tasks in a scheduling list by nonincreasing order of rank_u values.

class Task:
    def __init__(self, num):
        self.id = num
        self.processor = None
        self.ast = None     # Actual Start Time
        self.aft = None     # Actual Finish Time
        self.est = []       # Earliest execution Start Time
        self.eft = []       # Earliest execution Finish Time
        self.dl = None
        self.ranku = None
        self.rankd = None
        self.comp_cost = []
        self.avg_comp_cost = None
        self.successors = []
        self.predecessors = []
        self.assigned = False

    def __str__(self):
        return str(" TASK id: {}, succ: {}, pred: {}, avg_comp_cost: {}, ranku: {}, rankd: {}".format(
            self.id, self.successors, self.predecessors, self.avg_comp_cost, self.ranku, self.rankd
        ))


class Processor:
    def __init__(self, num):
        self.id = num
        self.tasks = []
        self.avail = 0      # processor ready time in a non-insertion based scheduling policy
    



def ranku(i, tasks):
    """Calculate Upward Rank of a task
    
    Arguments:
        i {int} -- task id
        tasks {list} -- list of Tasks
    """ 
    seq = [commcost(i, j,'a', 'b') + ranku(j, tasks) for j in tasks[i].successors]
    logging.debug('%s - seq: %s', i, seq)
    if i==0:
        return 9999
    if seq == []:
        return tasks[i].avg_comp_cost
    return tasks[i].avg_comp_cost + max(seq)


def rankd(i, tasks):
    """Calculate Downward Rank of a task
    
    Arguments:
        i {int} -- task id
        tasks {list} -- list of Tasks
    """
    if i==0:        # entry task
        return 0
    seq = [(rankd(j, tasks) + tasks[j].avg_comp_cost + commcost(j, i, 'a', 'b')) for j in tasks[i].predecessors]
    return max(seq)

def lft(i, tasks, D):
    if i == len(tasks) - 1: return D
    return min(tasks[j].lft - tasks[j].met - 0 for j in tasks[i].successors)
    # return min(tasks[j].lft - tasks[j].met - commcost_con(i, j) for j in tasks[i].successors)

def est(i, tasks):
    if i == 0: return 0
    return max(tasks[j].est + tasks[j].met + 0 for j in tasks[i].predecessors)
    # return max(tasks[j].est + tasks[j].met + commcost_con(j, i) for j in tasks[i].predecessors)

def eft(i, tasks):
    return tasks[i].est + tasks[i].met

def makespan(tasks):
    seq = [t.aft for t in tasks]
    return max(seq)

def assign(t, tasks, p, processors):
    tasks[t].est = max(est(t, tasks), processors[p].avail)
    tasks[t].eft = tasks[t].est + compcost(t, 'a')
    processors[p].tasks.append(tasks[t])
    processors[p].avail = tasks[t].eft
    tasks[t].assigned = True
    tasks[t].ast = tasks[t].est
    tasks[t].aft = tasks[t].eft

def hlfet():
    logging.info('------dls------')
    # Create Processors
    P = example.core
    processors = [Processor(i) for i in range(P)]
    # Create Tasks
    N = len(dag)
    tasks = [Task(i) for i in range(N+1)]

    for t, succ in dag.items():
        tasks[t].successors = [x for x in succ]
        agents = ''.join([chr(97+i) for i in range(P)]) # e.g., 'abc'
        tasks[t].comp_cost = [compcost(t, p) for p in agents]
        tasks[t].avg_comp_cost = stats.mean(tasks[t].comp_cost)   
        tasks[t].met = min(tasks[t].comp_cost)   
        for x in succ:
            tasks[x].predecessors.append(t)
        # setup entry task (id=0)
        tasks[0].avg_comp_cost = 0
        tasks[0].successors = [1]
        tasks[1].predecessors = [0]
        tasks[0].met = 0

    # Calculate ranku by traversing task graph upward
    for task in reversed(tasks):
        task.ranku = round(ranku(task.id, tasks), 3)
    
    # Calculate Rankd by traversing task graph upward
    for task in tasks:
        task.rankd = round(rankd(task.id, tasks), 3)
    
    # return a new sorted list, use the sorted() built-in function
    priority_list = sorted(tasks, key=lambda x: x.ranku, reverse=True)
    # priority_list = sorted(tasks, key=lambda x: x.rankd)

    D = 10 * sum(t.avg_comp_cost for t in tasks) # infinite deadline
    logging.info('D = {}'.format(D))

    # calculate EST
    for task in priority_list:
        tasks[task.id].est = est(task.id, tasks)
        tasks[task.id].eft = eft(task.id, tasks)

    logging.info('-'*7 + ' Tasks ' + '-'*7 )
    for task in tasks:
        logging.info(task)
    logging.info('-'*20)
    logging.info('task scheduling order: %s', [t.id for t in priority_list])

    remained = [i for i in range(N+1)]
    while len(remained) > 0:
        candidates = [(p, t, tasks[t].ranku) for p in processors for t in remained]
        to_assign = max(candidates, key=itemgetter(2))
        t, p = to_assign[1], to_assign[0].id
        assign(t, tasks, p, processors)
        remained.remove(t)

    for p in processors:
        for i in range(len(p.tasks)):
            p.tasks[i] = tasks[p.tasks[i].id]

    for p in processors:
        logging.info('tasks on processor %s: %s', p.id, [{t.id: (t.ast, t.aft)} for t in p.tasks])

    logging.info('makespan: %s', makespan(tasks))
    return processors, tasks, priority_list


# import maxcut
# gid = 1
# core = 3
# impact_factor, arc_num, vertex_num = maxcut.graph_parameter(gid)
# graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph(gid, vertex_num, arc_num, impact_factor)
# total_calculation_cost = sum(vertex_cpu)
# example.init_dag(graph, communication_cpu, core)
# dls()

# from heft import heft
# heft()