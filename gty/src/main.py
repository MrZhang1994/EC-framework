import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag, verbose
from heft import heft
from containerize import *
import draw
import os
from datetime import datetime

cores = [2,    3,   4,    5,   6]
mem   = [1, 0.95, 0.9, 0.85,  0.8, 0.75]
isol  = [1.5,  3,   5,  7.5, 10.5]
tests = [[0, 2, 1], [1, 2, 1], [2, 2, 1], [3, 2, 1], [4, 2, 1], [2, 0, 1], [2, 1, 1], [2, 3, 1], [2, 4, 1], [2, 5, 1], [2, 2, 0], [2, 2, 2], [2, 2, 3], [2, 2, 4]]

def main(k, gid):
    core = cores[tests[k][0]]
    Mem = mem[tests[k][1]]
    iso_limit = isol[tests[k][2]]

    path = './results_heft/graph' + str(gid) + '/' + str(k) + '/'

    # init graph
    impact_factor, arc_num, vertex_num = maxcut.graph_parameter(gid)
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph(gid, vertex_num, arc_num, impact_factor)

    # calculate maxtopcut
    S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    M = cut * Mem

    # calculate backward edge
    init_minLevel(vertex_num, graph)
    tmpu = 0
    tmpv = 0
    while cut > M:
        if verbose:
            print(S, T)
        u, v = minLevel(graph, S, T, 0, vertex_num-1)
        if (u == 0 and v == 0) or (tmpu == u and tmpv == v):
            if verbose:
                print('MinLevel Heuristic Failed\n')
            return -1
        tmpu = u
        tmpv = v
        maxcut.update_graph(graph, u, v)
        S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    
    # init example for heft
    example.init_dag(graph, communication_cpu, core)

    processors, tasks, priority_list = heft()
    order = [t.id for t in priority_list]

    lower = tasks[vertex_num].aft
    
    dag_d, r_dag, index, t, N, cpath = containerize_init(dag, tasks, processors, iso_limit, graph)
    

    # containerize
    cont, bridge_tasks, new_tasks = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'forward')
    if verbose:
        print('forward:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'forward.png')
        print(new_tasks[vertex_num].aft)
        print(cont)
    cont_open_f = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan_f = new_tasks[vertex_num].aft

    # containerize
    cont, bridge_tasks, new_tasks = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'backward')
    if verbose:
        print('backward:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'backward.png')
        print(new_tasks[vertex_num].aft)
        print(cont)
    cont_open_b = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan_b = new_tasks[vertex_num].aft

    if makespan_f < makespan_b:
        makespan_fb, cont_open_fb = makespan_f, cont_open_f
    else:
        makespan_fb, cont_open_fb = makespan_b, cont_open_b

    # containerize
    cont, bridge_tasks, new_tasks = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'i2c')
    if verbose:
        print('idle/comm:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'i2c.png')
        print(new_tasks[vertex_num].aft)
        print(cont)
    cont_open_i2c = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan_i2c = new_tasks[vertex_num].aft

    # in order
    cont, bridge_tasks, new_tasks = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'inorder')
    if verbose:
        print('in order:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'inorder.png')
        print(new_tasks[vertex_num].aft)
        print(cont)
    cont_open_i = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan_i = new_tasks[vertex_num].aft

    # random
    cont, bridge_tasks, new_tasks = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'rand')
    if verbose:
        print('random:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'random.png')
        print(new_tasks[vertex_num].aft)
        print(cont)
    cont_open_r = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan_r = new_tasks[vertex_num].aft

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

    """
    # spectral clustering
    Graph = graph
    Graph = [[i if (i != -1) else 0 for i in x ] for x in Graph]
    Graph = Graph + np.transpose(Graph)
    cont, bridge_tasks, new_tasks = containerize(tasks, processors, dag, dag_d, r_dag, index, t, N, order, 'sc', Graph)
    if verbose:
        print('sc:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'sc.png')
        print(new_tasks[vertex_num].aft)
        print(cont)
    cont_open_s = sum(draw.cal_cont_open([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont))
    makespan_s = new_tasks[vertex_num].aft
    """

    if verbose:
        print('-'*10)
        print('lower: ')
        print(lower)
        print('upper: ')
        print(upper)
        print('fb: ')
        print(round((makespan_fb - lower)/(upper - lower), 4))
        print('i2c: ')
        print(round((makespan_i2c - lower)/(upper - lower), 4))
        print('inorder: ')
        print(round((makespan_i - lower)/(upper - lower), 4))
        # print('sc: ')
        # print(round((makespan_s - lower)/(upper - lower), 4))
        print('random: ')
        print(round((makespan_r - lower)/(upper - lower), 4))
    
        with open(path + 'output.txt', 'a') as f:
            f.write(str(lower))
            f.write(str(upper))
            f.write(str(round((makespan_f - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_b - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_i2c - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_i - lower)/(upper - lower), 4)))
            # f.write(str(round((makespan_s - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_r - lower)/(upper - lower), 4)))

    with open(path + 'lower.txt', 'a') as f:
        f.write(str(lower) + '\n')
    
    with open(path + 'upper.txt', 'a') as f:
        f.write(str(upper) + '\n')
    
    with open(path + 'fb.txt', 'a') as f:
        f.write(str(round((makespan_fb - lower)/(upper - lower), 4)) + '\n')
    
    with open(path + 'fb_open.txt', 'a') as f:
        f.write(str(cont_open_fb) + '\n')
    
    with open(path + 'i2c.txt', 'a') as f:
        f.write(str(round((makespan_i2c - lower)/(upper - lower), 4)) + '\n')
    
    with open(path + 'i2c_open.txt', 'a') as f:
        f.write(str(cont_open_i2c) + '\n')

    with open(path + 'inorder.txt', 'a') as f:
        f.write(str(round((makespan_i - lower)/(upper - lower), 4)) + '\n')
    
    with open(path + 'inorder_open.txt', 'a') as f:
        f.write(str(cont_open_i) + '\n')
    """
    with open(path + 'sc.txt', 'a') as f:
        f.write(str(round((makespan_s - lower)/(upper - lower), 4)) + '\n')
    
    with open(path + 'sc_open.txt', 'a') as f:
        f.write(str(cont_open_s) + '\n')
    """
    with open(path + 'random.txt', 'a') as f:
        f.write(str(round((makespan_r - lower)/(upper - lower), 4)) + '\n')
    
    with open(path + 'random_open.txt', 'a') as f:
        f.write(str(cont_open_r) + '\n')
    
    return 0

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        os.system('rm -rf ' + path + '/*')

if __name__ == '__main__':
    random.seed(datetime.now())
    num = 200
    create_dir('./results_heft')
    for gid in [1, 2, 3, 4]:
        create_dir('./results_heft/graph' + str(gid))
        for k in range(len(tests)):
            create_dir('./results_heft/graph' + str(gid) + '/' + str(k))
            cnt = 0
            while cnt < num:
                try:
                    if main(k, gid) == 0:
                        cnt += 1
                except:
                    continue
