import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag
from heft import heft
from containerize import *
import draw

def main():
    iso_limit = 3
    # init graph
    impact_factor, arc_num, vertex_num, core = maxcut.graph2_parameter()
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph_2(vertex_num, arc_num, impact_factor)

    # calculate maxtopcut
    S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    M = cut * 0.9

    # calculate backward edge
    init_minLevel(vertex_num, graph)
    tmpu = 0
    tmpv = 0
    while cut > M:
        print(S, T)
        u, v = minLevel(graph, S, T, 0, vertex_num-1)
        if u == 0 and v == 0:
            print('MinLevel Heuristic Failed\n')
            return -1
        if tmpu == u and tmpv == v:
            return -2
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
    print('forward:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'forward.png')
    makespan_f = new_tasks[vertex_num].aft
    print(new_tasks[vertex_num].aft)
    print(cont)

    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'backward', iso_limit)
    print('backward:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'backward.png')
    makespan_b = new_tasks[vertex_num].aft
    print(new_tasks[vertex_num].aft)
    print(cont)

    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'i2c', iso_limit)
    print('idle/comm:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'i2c.png')
    makespan_i2c = new_tasks[vertex_num].aft
    print(new_tasks[vertex_num].aft)
    print(cont)

    # in order
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'inorder', iso_limit)
    print('in order:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'inorder.png')
    makespan_i = new_tasks[vertex_num].aft
    print(new_tasks[vertex_num].aft)
    print(cont)

    # random
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'rand', iso_limit)
    print('random:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'random.png')
    makespan_r = new_tasks[vertex_num].aft
    print(new_tasks[vertex_num].aft)
    print(cont)

    # upper bound
    cont = dict()
    for i in range(vertex_num+1):
        cont[i] = set()
        cont[i].add(i)
    one_tasks, one_processors = update_schedule(dag, r_dag, processors, tasks, range(1, vertex_num + 1), order, [i for i in range(vertex_num + 1)])
    print('upper bound:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in one_tasks], cont, 'upper.png')
    upper = one_tasks[vertex_num].aft
    print(one_tasks[vertex_num].aft)
    print(cont)

    print('-'*21)
    print('lower: ')
    print(lower)
    print('upper: ')
    print(upper)
    print('forward: ')
    print(round((makespan_f - lower)/(upper - lower), 4))
    print('backward: ')
    print(round((makespan_b - lower)/(upper - lower), 4))
    print('idle/communication: ')
    print(round((makespan_i2c - lower)/(upper - lower), 4))
    print('inorder: ')
    print(round((makespan_i - lower)/(upper - lower), 4))
    print('random: ')
    print(round((makespan_r - lower)/(upper - lower), 4))

    with open('./results/forward.txt', 'a') as f:
        f.write(str(round((makespan_f - lower)/(upper - lower), 4)) + '\n')
    
    with open('./results/backward.txt', 'a') as f:
        f.write(str(round((makespan_b - lower)/(upper - lower), 4)) + '\n')
    
    with open('./results/i2c.txt', 'a') as f:
        f.write(str(round((makespan_i2c - lower)/(upper - lower), 4)) + '\n')

    with open('./results/inorder.txt', 'a') as f:
        f.write(str(round((makespan_i - lower)/(upper - lower), 4)) + '\n')
    
    with open('./results/random.txt', 'a') as f:
        f.write(str(round((makespan_r - lower)/(upper - lower), 4)) + '\n')
    
    return 0

if __name__ == '__main__':
    for i in range(100):
        if main() == -2:
            print('OooooooOOooooops!')
            break
