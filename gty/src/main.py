import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag
from heft import heft
from containerize import *
import draw

def main():
    # init graph
    impact_factor, arc_num, vertex_num, core = maxcut.graph4_parameter()
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph_4(vertex_num, arc_num, impact_factor)

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

    # heft
    processors, tasks, priority_list = heft()
    order = [t.id for t in priority_list]
    
    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'forward', 2)
    print('forward:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'forward.png')
    print(new_tasks[vertex_num].aft)
    print(cont)

    # containerize
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'backward', 2)
    print('backward:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'backward.png')
    print(new_tasks[vertex_num].aft)
    print(cont)

    # in order
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'inorder', 2)
    print('in order:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'inorder.png')
    print(new_tasks[vertex_num].aft)
    print(cont)

    # random
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 'rand', 2)
    print('random:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks], cont, 'random.png')
    print(new_tasks[vertex_num].aft)
    print(cont)

    # upper bound
    one_tasks, one_processors = update_schedule(dag, r_dag, processors, tasks, range(1, vertex_num + 1), order, [i for i in range(vertex_num + 1)])
    print('upper bound:')
    draw.draw_canvas([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in one_tasks], cont, 'upper.png')
    print(one_tasks[vertex_num].aft)
    print(cont)
    

if __name__ == '__main__':
    main()
