import numpy as np
import random
from scipy.optimize import linprog

def graph1_parameter():
    impact_factor = 1.1
    arc_num = 18
    vertex_num = 12
    return impact_factor, arc_num, vertex_num

def initial_graph_1(graph, vertex_cpu, process, communication_cpu, vertex_num, arc_num, impact_factor): 
    vertex_cpu = []
    communication_cpu = []
    for i in range(vertex_num):
        vertex_cpu.append(random.randint(2,10))
        for j in range(vertex_num):
            graph[i, j] = -1
    '''       
    arc_weight = []
    for i in range(arc_num):
        arc_weight.append(random.randint(2,10))
    '''
    arc_weight = [3, 2, 7, 6, 8, 6, 9, 5, 7, 4, 5, 4, 8, 6, 8, 2, 8, 4]
    '''
    print('edge weight:')
    print(arc_weight)
    '''

    graph[0, 1] = arc_weight[0]
    graph[0, 2] = arc_weight[1]
    graph[0, 7] = arc_weight[2]
    graph[1, 2] = arc_weight[3]
    graph[1, 3] = arc_weight[4]
    graph[2, 4] = arc_weight[5]
    graph[2, 5] = arc_weight[6]
    graph[3, 6] = arc_weight[7]
    graph[3, 7] = arc_weight[8]
    graph[4, 8] = arc_weight[9]
    graph[6, 4] = arc_weight[10]
    graph[6, 9] = arc_weight[11]
    graph[7, 9] = arc_weight[12]
    graph[7, 10] = arc_weight[13]
    graph[5, 11] = arc_weight[14]
    graph[8, 11] = arc_weight[15]
    graph[9, 11] = arc_weight[16]
    graph[10, 11] = arc_weight[17]

    process[0] = (arc_weight[0] + arc_weight[1] + arc_weight[2]) * impact_factor
    process[1] = (arc_weight[3] + arc_weight[4]) * impact_factor
    process[2] = (arc_weight[5] + arc_weight[6]) * impact_factor
    process[3] = (arc_weight[7] + arc_weight[8]) * impact_factor
    process[4] = (arc_weight[9]) * impact_factor
    process[5] = (arc_weight[14]) * impact_factor
    process[6] = (arc_weight[10] + arc_weight[11]) * impact_factor
    process[7] = (arc_weight[12] + arc_weight[13]) * impact_factor
    process[8] = (arc_weight[15]) * impact_factor
    process[9] = (arc_weight[16]) * impact_factor
    process[10] = (arc_weight[17]) * impact_factor

    for i in range(vertex_num):
        communication_cpu.append(process[i] / impact_factor + vertex_cpu[i]) 

def maxtopocut(graph, process, vertex_num, core):
    augment_size = 2 * vertex_num
    augment_matrix = np.zeros((augment_size, augment_size))
    for i in range(augment_size):
        for j in range(augment_size):
            augment_matrix[i, j] = -1
    for i in range(vertex_num):
        for j in range(vertex_num):
            if graph[i, j] != -1:          
                index = i + vertex_num
                augment_matrix[index, j] = graph[i, j]
    for i in range(vertex_num):
        if process[i] != 0:
            augment_matrix[i, i + vertex_num] = process[i]
    A = np.zeros(augment_size)
    flag = 0
    in_degree = np.zeros(augment_size)
    out_degree = np.zeros(augment_size)
    for i in range(augment_size):
        for j in range(augment_size):
            if augment_matrix[i, j] != -1:
                Ai = np.zeros(augment_size)
                Ai[i] = -1
                Ai[j] = 1
                out_degree[i] += augment_matrix[i, j]
                in_degree[j] += augment_matrix[i, j]
                if flag == 0:
                    A = Ai
                    flag = 1
                else:
                    A = np.row_stack((A, Ai))
    A_core = np.zeros(augment_size)
    for k in range(vertex_num):
        if process[k] != 0:
            A_core[k] = 1
            A_core[k + vertex_num] = -1
    A = np.row_stack((A, A_core))
    b = np.zeros(A.shape[0])
    b[A.shape[0] - 1] = core
    lb = np.zeros(augment_size)
    ub = np.ones(augment_size)
    f = in_degree - out_degree
    bounds = np.row_stack((lb, ub))
    bounds = np.transpose(bounds)
    result = linprog(f, A, b, bounds = bounds)
    # print cut with process
    '''
    print('The S cut includes: ')
    for i in range(result.x.shape[0]):
        if result.x[i] >= 0.5:
            if i < vertex_num:
                print(str(i + 1), ', ', end = '')
            else:
                print(str(i - vertex_num + 1), '*, ', end = '')
    print('\n')            
    print('The T cut includes: ')
    for i in range(result.x.shape[0]):
        if result.x[i] < 0.5:
            if i < vertex_num:
                print(str(i + 1), ', ', end = '')
            else:
                print(str(i - vertex_num + 1), '*, ', end = '')
    '''
    # get valid cut
    valid_S = []
    valid_T = []
    for i in range(vertex_num):
        if result.x[i] >= 0.5 and result.x[i + vertex_num] >= 0.5:
            valid_S.append(i)
    for i in range(vertex_num):
        if i not in valid_S:
            valid_T.append(i)
    valid_cut = 0
    for i in range(vertex_num):
        for j in range(vertex_num):
            if graph[i, j] != -1 and i in valid_S and j in valid_T:
                valid_cut += graph[i, j]
    # print valid cut without process
    '''
    print('The valid S cut includes: ')
    for i in range(len(valid_S)):
        print(str(valid_S[i] + 1), ', ', end = '')
    print('\n')
    print('The valid T cut includes: ')
    for i in range(len(valid_T)):
        print(str(valid_T[i] + 1), ', ', end = '')
    print('\n')
    print('The valid cut has weight: ', str(valid_cut))
    '''
    # get origin cut
    origin_S = []
    origin_T = []
    for i in range(result.x.shape[0]):
        if result.x[i] >= 0.5:
            origin_S.append(i)
        else: 
            origin_T.append(i)
    origin_cut = 0
    for i in range(result.x.shape[0]):
        for j in range(result.x.shape[0]):
            if augment_matrix[i, j] != -1 and i in origin_S and j in origin_T:
                origin_cut += augment_matrix[i, j]

    return valid_S, valid_T, origin_cut


def main():
    impact_factor, arc_num, vertex_num = graph1_parameter()
    graph = np.zeros((vertex_num, vertex_num)) 
    vertex_cpu = np.zeros(vertex_num)
    process = np.zeros(vertex_num)
    communication_cpu = np.zeros(vertex_num)
    # communication_cpu used in scheduling, count the cost of communication in CPU working 
    initial_graph_1(graph, vertex_cpu, process, communication_cpu, vertex_num, arc_num, impact_factor)
    
    core_1 = 1
    core_2 = 2
    core_3 = 5

    S1, T1, cut1 = maxtopocut(graph, process, vertex_num, core_1)
    S2, T2, cut2 = maxtopocut(graph, process, vertex_num, core_2)
    S3, T3, cut3 = maxtopocut(graph, process, vertex_num, core_3)

    print(S1)
    print(T1)
    print(cut1)
    print(S2)
    print(T2)
    print(cut2)
    print(S3)
    print(T3)
    print(cut3)


if __name__ == '__main__':
    main()