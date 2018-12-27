import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag, verbose
from heft import heft
from containerize import *
import draw
import os

cores = [2,    3,   4,    5,   6]
mem   = [1, 0.95, 0.9, 0.85,  0.8, 0.75]
isol  = [1.5,  3,   5,  7.5, 10.5]
tests = [[0, 2, 1], [1, 2, 1], [2, 2, 1], [3, 2, 1], [4, 2, 1], [2, 0, 1], [2, 3, 1], [2, 4, 1], [2, 5, 1], [2, 2, 0], [2, 2, 2], [2, 2, 3], [2, 2, 4]]

def main(k, gid):
    core = cores[tests[k][0]]
    Mem = mem[tests[k][1]]
    iso_limit = isol[tests[k][2]]

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
    init_dag(graph, communication_cpu, core)

    # heft
    processors, tasks, priority_list = heft()
    order = [t.id for t in priority_list]

    lower = tasks[vertex_num].aft
    
    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'forward', iso_limit)
    if verbose:
        print('forward:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'forward.png')
        print(new_tasks[vertex_num].aft)
        print(cont)

    makespan_f = new_tasks[vertex_num].aft

    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'backward', iso_limit)
    if verbose:
        print('backward:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'backward.png')
        print(new_tasks[vertex_num].aft)
        print(cont)

    makespan_b = new_tasks[vertex_num].aft

    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'i2c', iso_limit)
    if verbose:
        print('idle/comm:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'i2c.png')
        print(new_tasks[vertex_num].aft)
        print(cont)

    makespan_i2c = new_tasks[vertex_num].aft

    # in order
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'inorder', iso_limit)
    if verbose:
        print('in order:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'inorder.png')
        print(new_tasks[vertex_num].aft)
        print(cont)

    makespan_i = new_tasks[vertex_num].aft

    # spectral clustering
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'sc', iso_limit, graph)
    if verbose:
        print('sc:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'sc.png')
        print(new_tasks[vertex_num].aft)
        print(cont)

    makespan_s = new_tasks[vertex_num].aft

    # random
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'rand', iso_limit)
    if verbose:
        print('random:')
        draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'random.png')
        print(new_tasks[vertex_num].aft)
        print(cont)
    makespan_r = new_tasks[vertex_num].aft

    # upper bound
    cont = dict()
    for i in range(vertex_num+1):
        cont[i] = set()
        cont[i].add(i)
    one_tasks, one_processors = update_schedule(dag, r_dag, processors, tasks, range(1, vertex_num + 1), order, [i for i in range(vertex_num + 1)])
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
        print('forward: ')
        print(round((makespan_f - lower)/(upper - lower), 4))
        print('backward: ')
        print(round((makespan_b - lower)/(upper - lower), 4))
        print('i2c: ')
        print(round((makespan_i2c - lower)/(upper - lower), 4))
        print('inorder: ')
        print(round((makespan_i - lower)/(upper - lower), 4))
        print('sc: ')
        print(round((makespan_s - lower)/(upper - lower), 4))
        print('random: ')
        print(round((makespan_r - lower)/(upper - lower), 4))
    
        with open('./results/'+str(k)+str(gid)+'output.txt', 'a') as f:
            f.write(str(lower))
            f.write(str(upper))
            f.write(str(round((makespan_f - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_b - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_i2c - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_i - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_s - lower)/(upper - lower), 4)))
            f.write(str(round((makespan_r - lower)/(upper - lower), 4)))

    with open('./results/'+str(k)+str(gid)+'lower.txt', 'a') as f:
        f.write(str(lower) + '\n')
    
    with open('./results/'+str(k)+str(gid)+'upper.txt', 'a') as f:
        f.write(str(upper) + '\n')

    with open('./results/'+str(k)+str(gid)+'forward.txt', 'a') as f:
        f.write(str(round((makespan_f - lower)/(upper - lower), 4)) + '\n')
    
    with open('./results/'+str(k)+str(gid)+'backward.txt', 'a') as f:
        f.write(str(round((makespan_b - lower)/(upper - lower), 4)) + '\n')
    
    with open('./results/'+str(k)+str(gid)+'i2c.txt', 'a') as f:
        f.write(str(round((makespan_i2c - lower)/(upper - lower), 4)) + '\n')

    with open('./results/'+str(k)+str(gid)+'inorder.txt', 'a') as f:
        f.write(str(round((makespan_i - lower)/(upper - lower), 4)) + '\n')
    
    with open('./results/'+str(k)+str(gid)+'sc.txt', 'a') as f:
        f.write(str(round((makespan_s - lower)/(upper - lower), 4)) + '\n')
    
    with open('./results/'+str(k)+str(gid)+'random.txt', 'a') as f:
        f.write(str(round((makespan_r - lower)/(upper - lower), 4)) + '\n')
    
    return 0

if __name__ == '__main__':
    num = 50
    for k in range(len(tests)):
        for gid in range(1, 5):
            os.system('rm -r ./results/'+str(k)+str(gid)+'*')
            cnt = 0
            while cnt < num:
                if main(k, gid) == 0:
                    cnt += 1
