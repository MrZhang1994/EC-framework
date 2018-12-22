from example import *
from heft import *
import numpy as np
import queue
import copy

def reverse_graph(dag, r_dag):
    for key in dag:
        for u in dag[key]:
            r_dag[u].add(key)
    return r_dag

def add_core_dependency(processors, dag, r_dag):
    dag[0] = set()
    print(dag)
    r_dag[0] = set()
    for p in processors:
        n = len(p.tasks)
        for i in range(1, n):
            r_dag[p.tasks[i].id].add(p.tasks[i-1].id)
            dag[p.tasks[i-1].id].add(p.tasks[i].id)
            
def cp(t, last, processors, tasks, step):
    if t == 0:
        res[step] = 0
        return True
    time_stamp = tasks[t].ast
    for i in range(len(last)):
        """
        print(last[i])
        print(processors[i].tasks[last[i]].id)
        print(tasks[processors[i].tasks[last[i]].id].aft)
        print('---')
        """
        while last[i] >= 0 and tasks[processors[i].tasks[last[i]].id].aft > time_stamp:
            last[i] -= 1
        if tasks[processors[i].tasks[last[i]].id].aft == time_stamp:
            if cp(processors[i].tasks[last[i]].id, last, processors, tasks, step+1) == True:
                res[step] = t
                return True
    return False
    
res = dict()
avg_cost = dict()

def get_avg_commcost(dag):
    for key in dag:
        n = len(dag[key])
        if n == 0:
            avg_cost[key] = 0
            continue
        s = sum([commcost_con(key, v) for v in dag[key]])
        avg_cost[key] = s / n;
        

def get_index(dag, tasks, cpath):
    influ_index = dict()
    N = len(tasks)
    for u in range(N):
        if not u in dag:
            continue
        tmp = sum([tasks[v].ast - tasks[u].aft for v in dag[u] if v in cpath])
        tmp -= avg_cost[u]
        n = sum([v in cpath for v in dag[u]])
        if n == 0:
            influ_index[u] = 0
        else:
            influ_index[u] = tmp/n
    index = []
    for key in influ_index:
        index.append(influ_index[key])
    return index

def init_iso(N):
    global iso_value
    iso_value = np.random.rand(N**2).reshape(N, N)
    iso_value = (iso_value + iso_value.T)/2

def iso(u, v):
    return 0.5
    global iso_value
    return iso_value[u, v]

def bfs(r_dag, tasks, index, t):
    N = len(tasks)
    Vc = [t] + [x for x in range(N-1) if index[x] < 0]
    Vc = sorted(Vc, key = lambda x: tasks[x].aft, reverse = True)
    Vp = [x for x in range(N) if x not in Vc]
    Vp = sorted(Vp, key = lambda x: tasks[x].aft, reverse = True)
    iso_limit = 2
    cont = dict()
    vis = set()
    cnt = 0
    print(Vc)
    cont[cnt] = set()
    iso_sum = 0
    for vc in Vc + Vp:
        q = queue.Queue()
        if vc in vis: continue
        delta = 0
        for task in cont[cnt]:
            delta += iso(task, vc)
        if iso_sum + delta > iso_limit: # new container
            iso_sum = 0
            cnt += 1
            cont[cnt] = set()
        
        iso_sum += delta
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

                if iso_sum + delta <= iso_limit:
                    exceeded = False
                    iso_sum += delta
                    cont[cnt].add(p)
                    vis.add(p)
                    q.put(p)
                else:
                    exceeded = True
            if exceeded and (cont[cnt] != set()):
                iso_sum = 0
                cnt += 1
                cont[cnt] = set()
                break
    return cont

def get_bridge_tasks(d, N, cont):
    bridge_tasks = []
    cont_set = dict()
    for c in cont:
        for task in cont[c]:
            cont_set[task] = c
    for u in d:
        for v in d[u]:
            if cont_set[u] != cont_set[v]:
                bridge_tasks.append(u)
                break
    return bridge_tasks

def containerize(d, processors, tasks, s, order):
    global iso_value
    N = len(tasks)
    init_iso(N)
    dag = dict()
    for k in d:
        for v in d[k]:
            try:
                dag[k].add(v)
            except:
                dag[k] = set()
                dag[k].add(v)
    r_dag = dict([(i, set()) for i in range(N)])
    reverse_graph(dag, r_dag)
    add_core_dependency(processors, dag, r_dag)
    get_avg_commcost(dag)
    
    # get critical path
    t = max(enumerate(tasks), key = lambda x: x[1].aft)[0]
    last = [len(p.tasks)-1 for p in processors]
    cp(t, last, processors, tasks, 0)
    cpath = []
    for key in res:
        cpath.append(res[key])
    
    index = get_index(dag, tasks, cpath)
    cont = bfs(r_dag, tasks, index, t)

    bridge_tasks = get_bridge_tasks(d, N, cont)
    # print(iso_value)
    new_tasks, new_processors = update_schedule(r_dag, processors, tasks, bridge_tasks, order)

    return r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors

def update_schedule(r_dag, processors, tasks, bridge_tasks, order):
    new_tasks = copy.deepcopy(tasks)
    new_processors = copy.deepcopy(processors)
    fact = 1.1
    w = [task.aft - task.ast for task in tasks]
    for i, x in enumerate(w):
        if i in bridge_tasks:
            x *= fact

    for i, p in enumerate(processors):
        for t in p.tasks:
            new_tasks[t.id].aft = 0
    
    for t in order:
        new_tasks[t].ast = max([new_tasks[x].aft for x in r_dag[t]]) if r_dag[t] != set() else 0
        new_tasks[t].aft = new_tasks[t].ast + w[t]
    
    for p in new_processors:
        for t in p.tasks:
            t.ast = new_tasks[t.id].ast
            t.aft = new_tasks[t.id].aft

    return new_tasks, new_processors