from example import *
from heft import *
import maxcut
import numpy as np
import queue
import copy
import random
from wr_sc import sc
import itertools

def reverse_graph(dag, r_dag):
    for key in dag:
        for u in dag[key]:
            r_dag[u].add(key)
    return r_dag

def add_core_dependency(processors, dag, r_dag, graph):
    dag[0] = set()
    r_dag[0] = set()
    for p in processors:
        n = len(p.tasks)
        for i in range(1, n):
            r_dag[p.tasks[i].id].add(p.tasks[i-1].id)
            dag[p.tasks[i-1].id].add(p.tasks[i].id)
            graph[p.tasks[i-1].id - 1][p.tasks[i].id - 1] = 0
            
def cp(t, last, processors, tasks, step, res):
    if t == 0:
        res[step] = 0
        return True
    time_stamp = tasks[t].ast
    for i in range(len(last)):
        while last[i] >= 0 and tasks[processors[i].tasks[last[i]].id].aft > time_stamp:
            last[i] -= 1
        if tasks[processors[i].tasks[last[i]].id].aft == time_stamp:
            if cp(processors[i].tasks[last[i]].id, last, processors, tasks, step+1, res) == True:
                res[step] = t
                return True
    return False
    

def get_avg_commcost(tasks, dag):
    avg_cost = dict()
    for key in dag:
        n = len(dag[key])
        if n == 0:
            avg_cost[key] = 0
            continue
        s = tasks[key].aft - tasks[key].ast + sum([commcost_con(key, v) for v in dag[key]]) * 2.7
        avg_cost[key] = s / n;
    return avg_cost
        

def get_index(dag, tasks, cpath, avg_cost):
    influ_index = dict()
    N = len(tasks)
    for u in range(N):
        if not u in dag:
            continue
        tmp = sum([tasks[v].ast - tasks[u].aft for v in dag[u] if v in cpath and tasks[u].processor == tasks[v].processor])
        tmp -= avg_cost[u]
        n = sum([v in cpath for v in dag[u]])
        if n == 0:
            influ_index[u] = 0
        else:
            influ_index[u] = tmp/n
    index = []
    for key in influ_index:
        index.append(influ_index[key])
    index.append(0)
    return index

def iso(u, v):
    if u == 0 or v == 0:
        return 0
    return maxcut.iso_value[u-1, v-1]

def bfs_forward(dag, tasks, index, t):
    global iso_limit
    N = len(tasks)
    Vc = [t] + [x for x in range(N-1) if index[x] < 0]
    Vc = sorted(Vc, key = lambda x: tasks[x].ast, reverse = False)
    Vp = [x for x in range(N) if x not in Vc]
    Vp = sorted(Vp, key = lambda x: tasks[x].aft, reverse = True)
    cont = dict()
    vis = set()
    cnt = 0
    cont[cnt] = set()
    iso_sum = 0
    
    q = queue.Queue()
    for vc in Vc + Vp:
        if vc in vis: continue
        delta = 0
        for task in cont[cnt]:
            delta += iso(task, vc)
        iso_sum += delta
        if iso_sum > iso_limit: # new container
            iso_sum = 0
            cnt += 1
            cont[cnt] = set()
        
        cont[cnt].add(vc)
        vis.add(vc)
        q.put(vc)
        while not q.empty():
            u = q.get()
            if not u in dag: continue
            children = sorted(dag[u], key = lambda x: index[x])
            exceeded = False
            for p in children:
                if p in vis: continue
                delta = 0
                for task in cont[cnt]:
                    delta += iso(task, p)

                iso_sum += delta

                if iso_sum > iso_limit:
                    exceeded = True
                    break
                cont[cnt].add(p)
                vis.add(p)
                q.put(p)
            
            if exceeded:
                q.queue.clear()
                iso_sum = 0
                if cont[cnt] != set():
                    cnt += 1
                    cont[cnt] = set()
                break
    return cont

def bfs_backward(r_dag, tasks, index, t):
    global iso_limit
    N = len(tasks)
    Vc = [t] + [x for x in range(N-1) if index[x] < 0]
    Vc = sorted(Vc, key = lambda x: tasks[x].aft, reverse = True)
    Vp = [x for x in range(N) if x not in Vc]
    Vp = sorted(Vp, key = lambda x: tasks[x].ast, reverse = False)
    cont = dict()
    vis = set()
    cnt = 0
    cont[cnt] = set()
    iso_sum = 0
    
    q = queue.Queue()
    for vc in Vc + Vp:
        if vc in vis: continue
        delta = 0
        for task in cont[cnt]:
            delta += iso(task, vc)
        iso_sum += delta
        if iso_sum > iso_limit: # new container
            iso_sum = 0
            cnt += 1
            cont[cnt] = set()
        
        cont[cnt].add(vc)
        vis.add(vc)
        q.put(vc)
        while not q.empty():
            u = q.get()
            if not u in r_dag: continue
            parents = sorted(r_dag[u], key = lambda x: index[x])
            exceeded = False
            for p in parents:
                if p in vis: continue
                delta = 0
                for task in cont[cnt]:
                    delta += iso(task, p)

                iso_sum += delta

                if iso_sum > iso_limit:
                    exceeded = True
                    break
                cont[cnt].add(p)
                vis.add(p)
                q.put(p)
            
            if exceeded:
                q.queue.clear()
                iso_sum = 0
                if cont[cnt] != set():
                    cnt += 1
                    cont[cnt] = set()
                break
    return cont

def bfs_i2c(r_dag, processors, tasks, t):
    global iso_limit

    idle = dict()
    # get idle
    for p in processors:
        if len(p.tasks) == 0: continue
        for i in range(len(p.tasks)-1):
            idle[p.tasks[i].id] = p.tasks[i+1].ast - p.tasks[i].aft
        if p.tasks[-1].id != t:
            idle[p.tasks[-1].id] = tasks[t].ast - p.tasks[-1].aft

    N = len(tasks)
    V = [x for x in range(N)]
    V = sorted(V, key = lambda x: tasks[x].aft, reverse = True)
    cont = dict()
    vis = set()
    cnt = 0
    cont[cnt] = set()
    iso_sum = 0
    
    q = queue.Queue()
    for vc in V:
        if vc in vis: continue
        delta = 0
        for task in cont[cnt]:
            delta += iso(task, vc)
        iso_sum += delta
        if iso_sum > iso_limit: # new container
            iso_sum = 0
            cnt += 1
            cont[cnt] = set()
        
        cont[cnt].add(vc)
        vis.add(vc)
        q.put(vc)
        while not q.empty():
            u = q.get()
            if not u in r_dag: continue
            parents = sorted(r_dag[u], key = lambda x: idle[x]/commcost_con(x, u) if commcost_con(x, u) != 0 else 10000)
            exceeded = False
            for p in parents:
                if p in vis: continue
                delta = 0
                for task in cont[cnt]:
                    delta += iso(task, p)

                iso_sum += delta

                if iso_sum > iso_limit:
                    exceeded = True
                    break
                cont[cnt].add(p)
                vis.add(p)
                q.put(p)
            
            if exceeded:
                q.queue.clear()
                iso_sum = 0
                if cont[cnt] != set():
                    cnt += 1
                    cont[cnt] = set()
                break
    return cont


def inorder(tasks):
    global iso_limit
    N = len(tasks)
    cont = dict()
    cnt = 0
    cont[cnt] = set()
    iso_sum = 0
    lst = [x for x in range(N)]
    lst = sorted(lst, key = lambda x: tasks[x].ast, reverse = False)
    for vc in lst:
        delta = 0
        for task in cont[cnt]:
            delta += iso(task, vc)
        iso_sum += delta

        if iso_sum > iso_limit: # new container
            iso_sum = 0
            cnt += 1
            cont[cnt] = set()
        
        cont[cnt].add(vc)
    return cont

def rd(tasks):
    global iso_limit
    N = len(tasks)
    cont = dict()
    cnt = 0
    cont[cnt] = set()
    iso_sum = 0
    lst = [x for x in range(N)]
    random.shuffle(lst)
    for vc in lst:
        delta = 0
        for task in cont[cnt]:
            delta += iso(task, vc)
        iso_sum += delta

        if iso_sum > iso_limit: # new container
            iso_sum = 0
            cnt += 1
            cont[cnt] = set()
        
        cont[cnt].add(vc)
    return cont

def cont_iso_sum(x):
    s = 0
    for pair in itertools.combinations(x, 2):
        s += iso(pair[0], pair[1])
        if s > iso_limit:
            return False
    return True

def optimal(vertex_num, tasks, processors, d, r_dag, order):
    search_cnt = 0
    best_makespan = 1e4
    # mapp = random.shuffle([i for i in range(len(tasks)-1)])
    for combination in itertools.product(*([[0,1,2,3] for _ in range(len(tasks)-1)])):
        if (0 not in combination) or (1 not in combination) or (2 not in combination): continue
        # if (0 not in combination) or (1 not in combination): continue
        flag = False
        for pair in maxcut.conflict_pairs:
            if combination[pair[0]] == combination[pair[1]]:
                flag = True
                break
        if flag: continue

        cont = dict()
        for i, x in enumerate(combination):
            if x not in cont:
                cont[x] = set()
            cont[x].add(i+1)

        iso_flag = False
        for key in cont:
            if cont_iso_sum(cont[key]) == False:
                iso_flag = True
                break
        if iso_flag: continue
        search_cnt += 1
        
        cont_set, bridge_tasks = get_bridge_tasks(d, len(tasks), cont)
        new_tasks = update_schedule(d, r_dag, processors, tasks, bridge_tasks, order, cont_set)
        makespan = new_tasks[vertex_num].aft
        if makespan < best_makespan:
            best_makespan = makespan
            # print(best_makespan, cont)
        if search_cnt > 2e3: return best_makespan
             
    return best_makespan

def get_bridge_tasks(d, N, cont):
    bridge_tasks = []
    cont_set = dict()
    for c in cont:
        for task in cont[c]:
            cont_set[task] = c
    for u in d:
        for v in d[u]:
            if cont_set[u] != cont_set[v] and commcost_con(u, v) != 0:
                bridge_tasks.append(u)
                break
    return cont_set, bridge_tasks

def containerize_init(d, tasks, processors, limit, graph):
    global iso_limit
    iso_limit = limit
    N = len(tasks)
    dag = dict(d)
    r_dag = dict([(i, set()) for i in range(N)])

    reverse_graph(dag, r_dag)
    add_core_dependency(processors, dag, r_dag, graph)
    avg_cost = get_avg_commcost(tasks, dag)
    
    # get critical path
    t = max(enumerate(tasks), key = lambda x: x[1].aft)[0]
    last = [len(p.tasks)-1 for p in processors]
    res = dict()
    cp(t, last, processors, tasks, 0, res)
    cpath = []
    for key in res:
        cpath.append(res[key])
    
    index = get_index(dag, tasks, cpath, avg_cost)
    return dag, r_dag, index, t, N, cpath

def containerize(tasks, processors, d, dag, r_dag, index, t, N, order, flag, Graph = example.graph):
    if flag == 'STO':
        cont = inorder(tasks)
    elif flag == 'rand':
        cont = rd(tasks)
    elif flag == 'forward':
        cont = bfs_forward(dag, tasks, index, t)
    elif flag == 'backward':
        cont = bfs_backward(r_dag, tasks, index, t)
    elif flag == 'ICRB':
        cont = bfs_i2c(r_dag, processors, tasks, t)
    else:
        cont = sc(Graph, maxcut.iso_value, iso_limit)

    cont_set, bridge_tasks = get_bridge_tasks(d, N, cont)

    new_tasks = update_schedule(d, r_dag, processors, tasks, bridge_tasks, order, cont_set)

    return cont, bridge_tasks, new_tasks

def update_schedule(d, r_dag, processors, tasks, bridge_tasks, order, cont_set):
    new_tasks = copy.deepcopy(tasks)
    new_processors = copy.deepcopy(processors)
    fact = 2.7
    w = [task.aft - task.ast for task in tasks]
    for i in bridge_tasks:
        w[i] += sum([commcost_con(i, v) for v in d[i] if cont_set[i] != cont_set[v]]) * fact

    for i, p in enumerate(processors):
        for t in p.tasks:
            new_tasks[t.id].aft = 0
    
    for t in order:
        new_tasks[t].ast = max([new_tasks[x].aft for x in r_dag[t]]) if r_dag[t] != set() else 0
        new_tasks[t].aft = new_tasks[t].ast + w[t]
    
    return new_tasks# , new_processors