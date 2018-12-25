import maxcut
from minlevel import minLevel, init_minLevel
from example import init_dag, dag
from heft import heft
from containerize import *

def main():
    # init graph
    impact_factor, arc_num, vertex_num, core = maxcut.graph1_parameter()
    graph, vertex_cpu, process, communication_cpu = maxcut.initial_graph_1(vertex_num, arc_num, impact_factor)

    # calculate maxtopcut
    S, T, cut = maxcut.maxtopocut(graph, process, vertex_num, core)
    M = cut * 0.8

    # calculate backward edge
    init_minLevel(vertex_num)
    while cut > M:
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
    r_dag, cpath, index, cont, bridge_tasks, new_tasks, new_processors = containerize(dag, processors, tasks, order, 3, 'bfs')

    print([(x.id, round(x.ast, 1), round(x.aft, 1), x.processor) for x in new_tasks])

if __name__ == '__main__':
    main()
