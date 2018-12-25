import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag
from cpop import cpop
from containerize import *
import draw

def main():
    iso_limit = 3
    # init graph
    impact_factor, arc_num, vertex_num, core = maxcut.graph1_parameter()
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph_1(vertex_num, arc_num, impact_factor)

    # calculate maxtopcut
    S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    M = cut * 0.9

    # calculate backward edge
    init_minLevel(vertex_num, graph)
    while cut > M:
        print(S, T)
        u, v = minLevel(graph, S, T, 0, vertex_num-1)
        if u == 0 and v == 0:
            print('MinLevel Heuristic Failed\n')
            return
        maxcut.update_graph(graph, u, v)
        S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    
    # init example for heft
    init_dag(graph, communication_cpu, core)

    # cpop
    processors, tasks, priority_list = cpop()
    order = [t.id for t in priority_list]
    
    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'forward', iso_limit)
    print('forward:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'forward.png')
    print(new_tasks[vertex_num].aft)
    print(cont)

    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'backward', iso_limit)
    print('backward:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'backward.png')
    print(new_tasks[vertex_num].aft)
    print(cont)

    # in order
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'inorder', iso_limit)
    print('in order:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'inorder.png')
    print(new_tasks[vertex_num].aft)
    print(cont)

    # random
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'rand', iso_limit)
    print('random:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'random.png')
    print(new_tasks[vertex_num].aft)
    print(cont)

    # upper bound
    cont_set = dict()
    for i in range(vertex_num + 1):
        cont_set[i] = i
    one_tasks, one_processors = update_schedule(dag, r_dag, processors, tasks, range(1, vertex_num + 1), order, cont_set)
    print('upper bound:')
    # draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in one_tasks], cont, 'upper.png')
    print(one_tasks[vertex_num].aft)
    print(cont)
    

if __name__ == '__main__':
    main()
