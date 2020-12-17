import example
from example import dag, commcost, compcost
import statistics as stats
from decimal import Decimal, ROUND_DOWN
import logging
import numpy as np
import copy
import random

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(level=logging.ERROR)


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
        self.met = None
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


def critical_parent(i, tasks, unassigned_parents):
    return unassigned_parents[np.argmax([tasks[j].eft + 0 for j in unassigned_parents])]
    # return np.argmax([tasks[j].eft + commcost_con(j, i) for j in unassigned_parents])


def assign_parents(i, tasks, processors, D):
    unassigned_parents = [j for j in tasks[i].predecessors if not tasks[j].assigned]
    while len(unassigned_parents) > 0:
        pcp = []
        t_i = i
        while len(unassigned_parents) > 0:
            t_i = critical_parent(t_i, tasks, unassigned_parents)
            pcp.insert(0, t_i)
            unassigned_parents = [j for j in tasks[t_i].predecessors if not tasks[j].assigned]

        tasks, processors = assign_path(pcp, tasks, processors, D)

        for t in pcp:
            for j in tasks[t].successors:
                tasks[j].est = est(j, tasks)
                tasks[j].eft = eft(j, tasks)
            for j in tasks[t].predecessors:
                tasks[j].lft = lft(j, tasks, D)
            tasks, processors = assign_parents(t, tasks, processors, D)

        unassigned_parents = [j for j in tasks[i].predecessors if not tasks[j].assigned]
    return tasks, processors

def toposort(d):
    q = []
    topo = [0]
    degrees = [0 for i in range(len(d)+1)]
    for x in d:
        for y in d[x]:
            degrees[y] += 1

    
    for x in d:
        if degrees[x] == 0:
            q.append(x)

    while len(q) > 0:
        topo.append(q[0])
        for suc in d[q[0]]:
            degrees[suc] -= 1
            if degrees[suc] == 0:
                q.append(suc)
        q = q[1:]

    return topo

def update(dag_d_tmp, tasks, processors):
    topo = toposort(dag_d_tmp)
    for tid in topo:
        tasks[tid].est = est(tid, tasks)
        tasks[tid].eft = eft(tid, tasks)
    return max([t.eft for t in tasks if t.assigned]), tasks, processors, dag_d_tmp


def try_assign(pcp, pid, tasks, processors):
    global lineage, dag_d
    new_tasks = copy.deepcopy(tasks)
    new_processors = copy.deepcopy(processors)
    p = new_processors[pid]
    dag_d_tmp = copy.deepcopy(dag_d)
    last_insert = -1
    for to_assign in pcp:
        parent = -1
        for j in reversed(range(len(p.tasks))):
            if j <= last_insert: break
            if to_assign in lineage[p.tasks[j].id]:
                parent = j
                break
        
        if parent == -1:
            parent = last_insert
        p.tasks.insert(parent + 1, new_tasks[to_assign])
        
        if parent != -1: # preds
            dag_d_tmp[p.tasks[parent].id].add(to_assign)
            new_tasks[to_assign].predecessors.append(p.tasks[parent].id)
            new_tasks[p.tasks[parent].id].successors.append(to_assign)
        
        if parent < len(p.tasks) - 2: # succs
            dag_d_tmp[to_assign].add(p.tasks[parent+2].id)
            new_tasks[p.tasks[parent+2].id].predecessors.append(to_assign)
            new_tasks[to_assign].successors.append(p.tasks[parent+2].id)

        last_insert = parent + 1
    
    return update(dag_d_tmp, new_tasks, new_processors)


def assign_path(pcp, tasks, processors, D):
    global dag_d
    makespan_min = D
    tasks_candidate, processors_candidate, p_candidate, dag_candidate = [], [], None, {}
    for pid, p in enumerate(processors):
        makespan_sofar, new_tasks, new_processors, new_dag_d = try_assign(pcp, pid, tasks, processors)
        if makespan_sofar < makespan_min:
            makespan_min = makespan_sofar
            tasks_candidate, processors_candidate = new_tasks, new_processors
            p_candidate = p
            dag_candidate = new_dag_d

    tasks, processors = tasks_candidate, processors_candidate
    dag_d = dag_candidate

    for t in pcp:
        tasks[t].assigned = True
        tasks[t].processor = p_candidate
    
    return tasks, processors


def ic_pcp():
    logging.info('------ic-pcp------')
    global dag_d, lineage
    # Create Processors
    P = example.core
    processors = [Processor(i) for i in range(P)]
    # Create Tasks
    N = len(dag)
    tasks = [Task(i) for i in range(N+1)]


    dag_d = copy.deepcopy(dag)
    lineage = copy.deepcopy(dag)
    topo = toposort(dag)
    for t in reversed(topo):
        children = set()
        if t not in lineage:
            lineage[t] = set()
        for x in lineage[t]:
            children = children.union(lineage[x])
        lineage[t] = lineage[t].union(children)
    
    lineage[0] = set([i for i in range(1, N+1)])

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

    # calculate LFT
    for task in reversed(priority_list):
        tasks[task.id].lft = lft(task.id, tasks, D)
    
    # calculate EST
    for task in priority_list:
        tasks[task.id].est = est(task.id, tasks)
        tasks[task.id].eft = eft(task.id, tasks)

    logging.info('-'*7 + ' Tasks ' + '-'*7 )
    for task in tasks:
        logging.info(task)
    logging.info('-'*20)
    logging.info('task scheduling order: %s', [t.id for t in priority_list])

    tasks[0].ast, tasks[0].aft, tasks[0].assigned = 0, 0, True
    tasks[-1].ast, tasks[-1].assigned = D, True

    tasks, processors = assign_parents(tasks[-1].id, tasks, processors, D)
    
    topo = toposort(dag_d)
    for t in topo:
        tasks[t].ast = est(t, tasks)
        tasks[t].aft = eft(t, tasks)

    tasks[-1].aft = est(tasks[-1].id, tasks)

    for p in processors:
        for i in range(len(p.tasks)):
            p.tasks[i] = tasks[p.tasks[i].id]


    for p in processors:
        logging.info('tasks on processor %s: %s', p.id, [{t.id: (t.ast, t.aft)} for t in p.tasks])

    logging.info('makespan: %s', makespan(tasks))
    return processors, tasks, priority_list


# import maxcut
# from heft import heft
# gid = 1
# core = 3
# impact_factor, arc_num, vertex_num = maxcut.graph_parameter(gid)
# graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph(gid, vertex_num, arc_num, impact_factor)
# total_calculation_cost = sum(vertex_cpu)
# example.init_dag(graph, communication_cpu, core)
# ic_pcp()
# logging.info('------heft------')
# heft()