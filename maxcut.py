import numpy as np
import random
# from scipy.optimize import linprog
from example import verbose
from datetime import datetime
from math import ceil, floor

iso_value = np.zeros((1, 1))
cpu_factor = 10
conflict_pairs = []

def add_software_dependency(N):
    global iso_value, conflict_pairs
    INF = 1e4
    num = random.choice([floor(N/10), ceil(N/10)])
    for _ in range(num):
        conflict_pair = random.sample(range(N), 2)
        conflict_pairs.append(conflict_pair)
        iso_value[conflict_pair[0]][conflict_pair[1]] = INF
        iso_value[conflict_pair[1]][conflict_pair[0]] = INF

def init_iso(N):
    global iso_value
    iso_value = np.random.rand(N**2).reshape(N, N)
    iso_value = (iso_value + iso_value.T)/2
    iso_value -= np.diag(np.diag(iso_value))
    add_software_dependency(N)
    return iso_value

def graph_parameter(gid):
    if gid == 1:
        return graph1_parameter()
    if gid == 2:
        return graph2_parameter()
    if gid == 3:
        return graph3_parameter()
    if gid == 4:
        return graph4_parameter()
    if gid == 5:
        return graph5_parameter()

def initial_graph(gid, vertex_num, arc_num, impact_factor):
    if gid == 1:
        return initial_graph_1(vertex_num, arc_num, impact_factor)
    if gid == 2:
        return initial_graph_2(vertex_num, arc_num, impact_factor)
    if gid == 3:
        return initial_graph_3(vertex_num, arc_num, impact_factor)
    if gid == 4:
        return initial_graph_4(vertex_num, arc_num, impact_factor)
    if gid == 5:
        return initial_graph_5(vertex_num, arc_num, impact_factor)

def graph1_parameter():
    impact_factor = []
    arc_num = 14
    vertex_num = 11
    for i in range(vertex_num):
        impact_factor.append(random.uniform(0.8, 2))
    return impact_factor, arc_num, vertex_num

def graph2_parameter():
    impact_factor = []    
    arc_num = 56
    vertex_num = 25
    for i in range(vertex_num):
        impact_factor.append(random.uniform(0.8, 2))
    return impact_factor, arc_num, vertex_num

def graph3_parameter():
    impact_factor = []
    arc_num = 71
    vertex_num = 41
    for i in range(vertex_num):
        impact_factor.append(random.uniform(0.8, 2))
    return impact_factor, arc_num, vertex_num

def graph4_parameter():
    impact_factor = []
    arc_num = 34
    vertex_num = 19
    for i in range(vertex_num):
        impact_factor.append(random.uniform(0.8, 2))
    return impact_factor, arc_num, vertex_num

def list_sum(list, index):
    sum = 0
    for i in index:
        sum += list[i]
    return sum

def initial_graph_1(vertex_num, arc_num, impact_factor):
    global iso_value, cpu_factor
    graph = np.zeros((vertex_num, vertex_num))
    process = np.zeros(vertex_num)
    vertex_cpu = []
    communication_cpu = []
    for i in range(vertex_num):
        vertex_cpu.append(random.uniform(10, 100))
        for j in range(vertex_num):
            graph[i, j] = -1
          
    arc_weight = []
    for i in range(arc_num):
        arc_weight.append(random.uniform(10, 100)*random.choice([0.1, 0.5, 1, 5, 10]))
    '''
    arc_weight = [3, 2, 7, 6, 8, 6, 9, 5, 7, 4, 5, 4, 8, 6, 8, 2, 8, 4]
    print('edge weight:')
    print(arc_weight)
    '''
    
    graph[0, 1] = arc_weight[0]
    graph[0, 2] = arc_weight[1]
    graph[2, 1] = arc_weight[2]
    graph[1, 3] = arc_weight[3]
    graph[1, 4] = arc_weight[4]
    graph[1, 5] = arc_weight[5]
    graph[2, 10] = arc_weight[6]
    graph[3, 6] = arc_weight[7]
    graph[4, 7] = arc_weight[8]
    graph[5, 8] = arc_weight[9]
    graph[6, 9] = arc_weight[10]
    graph[7, 9] = arc_weight[11]
    graph[8, 9] = arc_weight[12]
    graph[9, 10] = arc_weight[13]
    
    
    process[0] = list_sum(arc_weight, [0, 1]) * impact_factor[0]
    process[1] = list_sum(arc_weight, [3, 4, 5]) * impact_factor[1]
    process[2] = list_sum(arc_weight, [2, 6]) * impact_factor[2]
    process[3] = list_sum(arc_weight, [7]) * impact_factor[3]
    process[4] = list_sum(arc_weight, [8]) * impact_factor[4]
    process[5] = list_sum(arc_weight, [9]) * impact_factor[5]
    process[6] = list_sum(arc_weight, [10]) * impact_factor[6]
    process[7] = list_sum(arc_weight, [11]) * impact_factor[7]
    process[8] = list_sum(arc_weight, [12]) * impact_factor[8]
    process[9] = list_sum(arc_weight, [13]) * impact_factor[9]
    process[10] = list_sum(arc_weight, [6, 13]) * impact_factor[10]

    iso_value = init_iso(vertex_num)
    
    for i in range(vertex_num):
        communication_cpu.append(vertex_cpu[i])
    if verbose:
        print('communication_cpu')
        print(communication_cpu)
        print('process')
        print(process)
        print('iso_value')
        print(iso_value)
    return graph, vertex_cpu, process, communication_cpu

def initial_graph_2(vertex_num, arc_num, impact_factor):
    global iso_value, cpu_factor
    graph = np.zeros((vertex_num, vertex_num))
    process = np.zeros(vertex_num)
    vertex_cpu = []
    communication_cpu = []
    for i in range(vertex_num):
        vertex_cpu.append(random.uniform(10, 100))
        for j in range(vertex_num):
            graph[i, j] = -1
    if verbose:
        print('vertex_cpu:')
        print(vertex_cpu)

    arc_weight = []
    for i in range(arc_num):
        arc_weight.append(random.uniform(10, 100)*random.choice([0.1, 0.5, 1, 5, 10]))
    if verbose:
        print('edge weight:')
        print(arc_weight)
    '''
    arc_weight = [3, 2, 7, 6, 8, 6, 9, 5, 7, 4, 5, 4, 8, 6, 8, 2, 8, 4]
    '''
    '''
    print('edge weight:')
    print(arc_weight)
    '''

    graph[0, 1] = arc_weight[0]
    graph[0, 2] = arc_weight[1]
    graph[0, 3] = arc_weight[2]
    graph[0, 4] = arc_weight[3]
    graph[0, 5] = arc_weight[4]
    graph[0, 6] = arc_weight[5]
    graph[1, 17] = arc_weight[6]
    graph[1, 7] = arc_weight[7]
    graph[1, 8] = arc_weight[8]
    graph[2, 8] = arc_weight[9]
    graph[2, 7] = arc_weight[10]
    graph[2, 18] = arc_weight[11]
    graph[2, 9] = arc_weight[12]
    graph[3, 8] = arc_weight[13]
    graph[3, 9] = arc_weight[14]
    graph[3, 10] = arc_weight[15]
    graph[3, 11] = arc_weight[16]
    graph[4, 19] = arc_weight[17]
    graph[4, 10] = arc_weight[18]
    graph[4, 12] = arc_weight[19]
    graph[4, 13] = arc_weight[20]
    graph[5, 11] = arc_weight[21]
    graph[5, 12] = arc_weight[22]
    graph[5, 21] = arc_weight[23]
    graph[5, 14] = arc_weight[24]
    graph[6, 13] = arc_weight[25]
    graph[6, 14] = arc_weight[26]
    graph[6, 22] = arc_weight[27]
    graph[7, 15] = arc_weight[28]
    graph[8, 15] = arc_weight[29]
    graph[9, 15] = arc_weight[30]
    graph[10, 15] = arc_weight[31]
    graph[11, 15] = arc_weight[32]
    graph[12, 15] = arc_weight[33]
    graph[13, 15] = arc_weight[34]
    graph[14, 15] = arc_weight[35]
    graph[15, 16] = arc_weight[36]
    graph[16, 17] = arc_weight[37]
    graph[16, 18] = arc_weight[38]
    graph[16, 19] = arc_weight[39]
    graph[16, 20] = arc_weight[40]
    graph[16, 21] = arc_weight[41]
    graph[16, 22] = arc_weight[42]
    graph[17, 23] = arc_weight[43]
    graph[18, 23] = arc_weight[44]
    graph[19, 23] = arc_weight[45]
    graph[20, 23] = arc_weight[46]
    graph[21, 23] = arc_weight[47]
    graph[22, 23] = arc_weight[48]
    graph[17, 24] = arc_weight[49]
    graph[18, 24] = arc_weight[50]
    graph[19, 24] = arc_weight[51]
    graph[20, 24] = arc_weight[52]
    graph[21, 24] = arc_weight[53]
    graph[22, 24] = arc_weight[54]
    graph[23, 24] = arc_weight[55]

    process[0] = list_sum(arc_weight, [0, 1, 2, 3, 4, 5]) * impact_factor[0]
    process[1] = list_sum(arc_weight, [6, 7, 8]) * impact_factor[1]
    process[2] = list_sum(arc_weight, [9, 10 ,11]) * impact_factor[2]
    process[3] = list_sum(arc_weight, [12, 13, 14, 15, 16]) * impact_factor[3]
    process[4] = list_sum(arc_weight, [17, 18, 19, 20]) * impact_factor[4]
    process[5] = list_sum(arc_weight, [21, 22, 23, 24]) * impact_factor[5]
    process[6] = list_sum(arc_weight, [25, 26, 27]) * impact_factor[6]
    process[7] = list_sum(arc_weight, [28]) * impact_factor[7]
    process[8] = list_sum(arc_weight, [29]) * impact_factor[8]
    process[9] = list_sum(arc_weight, [30]) * impact_factor[9]
    process[10] = list_sum(arc_weight, [31]) * impact_factor[10]
    process[11] = list_sum(arc_weight, [32]) * impact_factor[11]
    process[12] = list_sum(arc_weight, [33]) * impact_factor[12]
    process[13] = list_sum(arc_weight, [34]) * impact_factor[13]
    process[14] = list_sum(arc_weight, [35]) * impact_factor[14]
    process[15] = list_sum(arc_weight, [36]) * impact_factor[15]
    process[16] = list_sum(arc_weight, [37, 38, 39, 40, 41, 42]) * impact_factor[16]
    process[17] = list_sum(arc_weight, [43, 44]) * impact_factor[17]
    process[18] = list_sum(arc_weight, [45, 46]) * impact_factor[18]
    process[19] = list_sum(arc_weight, [47, 48]) * impact_factor[19]
    process[20] = list_sum(arc_weight, [49, 50]) * impact_factor[20]
    process[21] = list_sum(arc_weight, [51, 52]) * impact_factor[21]
    process[22] = list_sum(arc_weight, [53, 54]) * impact_factor[22]
    process[23] = list_sum(arc_weight, [55]) * impact_factor[23]

    iso_value = init_iso(vertex_num)

    for i in range(vertex_num):
        communication_cpu.append(vertex_cpu[i])
    if verbose:
        print('communication_cpu')
        print(communication_cpu)
        print('process')
        print(process)
        print('iso_value')
        print(iso_value)
    return graph, vertex_cpu, process, communication_cpu

def initial_graph_3(vertex_num, arc_num, impact_factor):
    global iso_value, cpu_factor
    graph = np.zeros((vertex_num, vertex_num))
    process = np.zeros(vertex_num)
    vertex_cpu = []
    communication_cpu = []
    for i in range(vertex_num):
        vertex_cpu.append(random.uniform(10, 100))
        for j in range(vertex_num):
            graph[i, j] = -1
    if verbose:
        print('vertex_cpu:')
        print(vertex_cpu)

    arc_weight = []
    for i in range(arc_num):
        arc_weight.append(random.uniform(10, 100)*random.choice([0.1, 0.5, 1, 5, 10]))
    if verbose:
        print('edge weight:')
        print(arc_weight)
    '''
    arc_weight = [3, 2, 7, 6, 8, 6, 9, 5, 7, 4, 5, 4, 8, 6, 8, 2, 8, 4]
    '''
    '''
    print('edge weight:')
    print(arc_weight)
    '''

    graph[0, 1] = arc_weight[0]
    graph[0, 2] = arc_weight[1]
    graph[0, 3] = arc_weight[2]
    graph[1, 4] = arc_weight[3]
    graph[1, 6] = arc_weight[4]
    graph[2, 5] = arc_weight[5]
    graph[2, 6] = arc_weight[6]
    graph[3, 7] = arc_weight[7]
    graph[3, 8] = arc_weight[8]
    graph[3, 9] = arc_weight[9]
    graph[3, 10] = arc_weight[10]
    graph[4, 11] = arc_weight[11]
    graph[5, 11] = arc_weight[12]
    graph[6, 12] = arc_weight[13]
    graph[6, 27] = arc_weight[14]
    graph[6, 28] = arc_weight[15]
    graph[7, 13] = arc_weight[16]
    graph[8, 13] = arc_weight[17]
    graph[9, 14] = arc_weight[18]
    graph[10, 14] = arc_weight[19]
    graph[11, 15] = arc_weight[20]
    graph[11, 16] = arc_weight[21]
    graph[11, 17] = arc_weight[22]
    graph[11, 18] = arc_weight[23]
    graph[11, 19] = arc_weight[24]
    graph[11, 20] = arc_weight[25]
    graph[12, 15] = arc_weight[26]
    graph[12, 16] = arc_weight[27]
    graph[12, 17] = arc_weight[28]
    graph[12, 18] = arc_weight[29]
    graph[12, 19] = arc_weight[30]
    graph[12, 20] = arc_weight[31]
    graph[13, 20] = arc_weight[32]
    graph[13, 21] = arc_weight[33]
    graph[14, 21] = arc_weight[34]
    graph[15, 22] = arc_weight[35]
    graph[15, 23] = arc_weight[36]
    graph[15, 24] = arc_weight[37]
    graph[16, 25] = arc_weight[38]
    graph[17, 25] = arc_weight[39]
    graph[18, 25] = arc_weight[40]
    graph[18, 26] = arc_weight[41]
    graph[19, 26] = arc_weight[42]
    graph[20, 26] = arc_weight[43]
    graph[20, 33] = arc_weight[44]
    graph[21, 27] = arc_weight[45]
    graph[21, 28] = arc_weight[46]
    graph[22, 29] = arc_weight[47]
    graph[23, 29] = arc_weight[48]
    graph[23, 30] = arc_weight[49]
    graph[24, 30] = arc_weight[50]
    graph[24, 31] = arc_weight[51]
    graph[25, 32] = arc_weight[52]
    graph[26, 32] = arc_weight[53]
    graph[27, 31] = arc_weight[54]
    graph[27, 32] = arc_weight[55]
    graph[27, 34] = arc_weight[56]
    graph[28, 33] = arc_weight[57]
    graph[28, 34] = arc_weight[58]
    graph[29, 35] = arc_weight[59]
    graph[30, 35] = arc_weight[60]
    graph[31, 36] = arc_weight[61]
    graph[32, 36] = arc_weight[62]
    graph[33, 37] = arc_weight[63]
    graph[34, 37] = arc_weight[64]
    graph[35, 38] = arc_weight[65]
    graph[36, 38] = arc_weight[66]
    graph[36, 39] = arc_weight[67]
    graph[37, 39] = arc_weight[68]
    graph[38, 40] = arc_weight[69]
    graph[39, 40] = arc_weight[70]

    process[0] = list_sum(arc_weight, [0, 1, 2]) * impact_factor[0]
    process[1] = list_sum(arc_weight, [3, 4]) * impact_factor[1]
    process[2] = list_sum(arc_weight, [5, 6]) * impact_factor[2]
    process[3] = list_sum(arc_weight, [7, 8, 9, 10]) * impact_factor[3]
    process[4] = list_sum(arc_weight, [11]) * impact_factor[4]
    process[5] = list_sum(arc_weight, [12]) * impact_factor[5]
    process[6] = list_sum(arc_weight, [13, 14, 15]) * impact_factor[6]
    process[7] = list_sum(arc_weight, [16]) * impact_factor[7]
    process[8] = list_sum(arc_weight, [17]) * impact_factor[8]
    process[9] = list_sum(arc_weight, [18]) * impact_factor[9]
    process[10] = list_sum(arc_weight, [19]) * impact_factor[10]
    process[11] = list_sum(arc_weight, [20, 21, 22, 23, 24, 25]) * impact_factor[11]
    process[12] = list_sum(arc_weight, [26, 27, 28, 29, 30, 31]) * impact_factor[12]
    process[13] = list_sum(arc_weight, [32, 33]) * impact_factor[13]
    process[14] = list_sum(arc_weight, [34]) * impact_factor[14]
    process[15] = list_sum(arc_weight, [35, 36, 37]) * impact_factor[15]
    process[16] = list_sum(arc_weight, [38]) * impact_factor[16]
    process[17] = list_sum(arc_weight, [39]) * impact_factor[17]
    process[18] = list_sum(arc_weight, [40, 41]) * impact_factor[18]
    process[19] = list_sum(arc_weight, [42]) * impact_factor[19]
    process[20] = list_sum(arc_weight, [43, 44]) * impact_factor[20]
    process[21] = list_sum(arc_weight, [45, 46]) * impact_factor[21]
    process[22] = list_sum(arc_weight, [47]) * impact_factor[22]
    process[23] = list_sum(arc_weight, [48, 49]) * impact_factor[23]
    process[24] = list_sum(arc_weight, [50, 51]) * impact_factor[24]
    process[25] = list_sum(arc_weight, [52]) * impact_factor[25]
    process[26] = list_sum(arc_weight, [53]) * impact_factor[26]
    process[27] = list_sum(arc_weight, [54, 55, 56]) * impact_factor[27]
    process[28] = list_sum(arc_weight, [57, 58]) * impact_factor[28]
    process[29] = list_sum(arc_weight, [59]) * impact_factor[29]
    process[30] = list_sum(arc_weight, [60]) * impact_factor[30]
    process[31] = list_sum(arc_weight, [61]) * impact_factor[31]
    process[32] = list_sum(arc_weight, [62]) * impact_factor[32]
    process[33] = list_sum(arc_weight, [63]) * impact_factor[33]
    process[34] = list_sum(arc_weight, [64]) * impact_factor[34]
    process[35] = list_sum(arc_weight, [65]) * impact_factor[35]
    process[36] = list_sum(arc_weight, [66, 67]) * impact_factor[36]
    process[37] = list_sum(arc_weight, [68]) * impact_factor[37]
    process[38] = list_sum(arc_weight, [69]) * impact_factor[38]
    process[39] = list_sum(arc_weight, [70]) * impact_factor[39]

    iso_value = init_iso(vertex_num)

    for i in range(vertex_num):
        communication_cpu.append(vertex_cpu[i])
    if verbose:
        print('communication_cpu')
        print(communication_cpu)
        print('process')
        print(process)
        print('iso_value')
        print(iso_value)
    return graph, vertex_cpu, process, communication_cpu

def initial_graph_4(vertex_num, arc_num, impact_factor):
    global iso_value, cpu_factor
    graph = np.zeros((vertex_num, vertex_num))
    process = np.zeros(vertex_num)
    vertex_cpu = []
    communication_cpu = []
    for i in range(vertex_num):
        vertex_cpu.append(random.uniform(10, 100))
        for j in range(vertex_num):
            graph[i, j] = -1
    if verbose:
        print('vertex_cpu:')
        print(vertex_cpu)

    arc_weight = []
    for i in range(arc_num):
        arc_weight.append(random.uniform(10, 100)*random.choice([0.1, 0.5, 1, 5, 10]))
    if verbose:
        print('edge weight:')
        print(arc_weight)
    '''
    arc_weight = [3, 2, 7, 6, 8, 6, 9, 5, 7, 4, 5, 4, 8, 6, 8, 2, 8, 4]
    '''
    '''
    print('edge weight:')
    print(arc_weight)
    '''

    graph[0, 1] = arc_weight[0]
    graph[0, 6] = arc_weight[1]
    graph[0, 2] = arc_weight[2]
    graph[0, 3] = arc_weight[3]
    graph[0, 4] = arc_weight[4]
    graph[0, 5] = arc_weight[5]
    graph[1, 18] = arc_weight[6]
    graph[2, 7] = arc_weight[7]
    graph[2, 6] = arc_weight[8]
    graph[3, 8] = arc_weight[9]
    graph[4, 9] = arc_weight[10]
    graph[5, 10] = arc_weight[11]
    graph[6, 7] = arc_weight[12]
    graph[6, 11] = arc_weight[13]
    graph[6, 8] = arc_weight[14]
    graph[6, 9] = arc_weight[15]
    graph[6, 10] = arc_weight[16]
    graph[7, 18] = arc_weight[17]
    graph[8, 12] = arc_weight[18]
    graph[8, 11] = arc_weight[19]
    graph[9, 13] = arc_weight[20]
    graph[10, 14] = arc_weight[21]
    graph[11, 12] = arc_weight[22]
    graph[11, 15] = arc_weight[23]
    graph[11, 13] = arc_weight[24]
    graph[11, 14] = arc_weight[25]
    graph[12, 18] = arc_weight[26]
    graph[13, 16] = arc_weight[27]
    graph[13, 15] = arc_weight[28]
    graph[14, 17] = arc_weight[29]
    graph[15, 16] = arc_weight[30]
    graph[15, 17] = arc_weight[31]
    graph[16, 18] = arc_weight[32]
    graph[17, 18] = arc_weight[33]

    process[0] = list_sum(arc_weight, [0, 1, 2, 3, 4, 5]) * impact_factor[0]
    process[1] = list_sum(arc_weight, [6]) * impact_factor[1]
    process[2] = list_sum(arc_weight, [7, 8]) * impact_factor[2]
    process[3] = list_sum(arc_weight, [9]) * impact_factor[3]
    process[4] = list_sum(arc_weight, [10]) * impact_factor[4]
    process[5] = list_sum(arc_weight, [11]) * impact_factor[5]
    process[6] = list_sum(arc_weight, [12, 13, 14, 15, 16]) * impact_factor[6]
    process[7] = list_sum(arc_weight, [17]) * impact_factor[7]
    process[8] = list_sum(arc_weight, [18, 19]) * impact_factor[8]
    process[9] = list_sum(arc_weight, [20]) * impact_factor[9]
    process[10] = list_sum(arc_weight, [21]) * impact_factor[10]
    process[11] = list_sum(arc_weight, [22, 23, 24, 25]) * impact_factor[11]
    process[12] = list_sum(arc_weight, [26]) * impact_factor[12]
    process[13] = list_sum(arc_weight, [27, 28]) * impact_factor[13]
    process[14] = list_sum(arc_weight, [29]) * impact_factor[14]
    process[15] = list_sum(arc_weight, [30, 31]) * impact_factor[15]
    process[16] = list_sum(arc_weight, [32]) * impact_factor[16]
    process[17] = list_sum(arc_weight, [33]) * impact_factor[17]

    iso_value = init_iso(vertex_num)

    for i in range(vertex_num):
        communication_cpu.append(vertex_cpu[i])
    if verbose:
        print('communication_cpu')
        print(communication_cpu)
        print('process')
        print(process)
        print('iso_value')
        print(iso_value)
    return graph, vertex_cpu, process, communication_cpu

# def maxtopocut(graph, process, vertex_num, core):
#     augment_size = 2 * vertex_num
#     augment_matrix = np.zeros((augment_size, augment_size))
#     for i in range(augment_size):
#         for j in range(augment_size):
#             augment_matrix[i, j] = -1
#     for i in range(vertex_num):
#         for j in range(vertex_num):
#             if graph[i, j] != -1:          
#                 index = i + vertex_num
#                 augment_matrix[index, j] = graph[i, j]
#     for i in range(vertex_num):
#         if process[i] != 0:
#             augment_matrix[i, i + vertex_num] = process[i]
#     A = np.zeros(augment_size)
#     flag = 0
#     in_degree = np.zeros(augment_size)
#     out_degree = np.zeros(augment_size)
#     for i in range(augment_size):
#         for j in range(augment_size):
#             if augment_matrix[i, j] != -1:
#                 Ai = np.zeros(augment_size)
#                 Ai[i] = -1
#                 Ai[j] = 1
#                 out_degree[i] += augment_matrix[i, j]
#                 in_degree[j] += augment_matrix[i, j]
#                 if flag == 0:
#                     A = Ai
#                     flag = 1
#                 else:
#                     A = np.row_stack((A, Ai))
#     A_core = np.zeros(augment_size)
#     for k in range(vertex_num):
#         if process[k] != 0:
#             A_core[k] = 1
#             A_core[k + vertex_num] = -1
#     A = np.row_stack((A, A_core))
#     b = np.zeros(A.shape[0])
#     b[A.shape[0] - 1] = core
#     lb = np.zeros(augment_size)
#     ub = np.ones(augment_size)
#     f = in_degree - out_degree
#     bounds = np.row_stack((lb, ub))
#     bounds = np.transpose(bounds)
#     result = linprog(f, A, b, bounds = bounds)
#     # print cut with process
#     '''
#     print('The S cut includes: ')
#     for i in range(result.x.shape[0]):
#         if result.x[i] >= 0.5:
#             if i < vertex_num:
#                 print(str(i + 1), ', ', end = '')
#             else:
#                 print(str(i - vertex_num + 1), '*, ', end = '')
#     print('\n')            
#     print('The T cut includes: ')
#     for i in range(result.x.shape[0]):
#         if result.x[i] < 0.5:
#             if i < vertex_num:
#                 print(str(i + 1), ', ', end = '')
#             else:
#                 print(str(i - vertex_num + 1), '*, ', end = '')
#     '''
#     # get valid cut
#     valid_S = []
#     valid_T = []
#     for i in range(vertex_num):
#         if result.x[i] >= 0.5 and result.x[i + vertex_num] >= 0.5:
#             valid_S.append(i)
#     for i in range(vertex_num):
#         if i not in valid_S:
#             valid_T.append(i)
#     valid_cut = 0
#     for i in range(vertex_num):
#         for j in range(vertex_num):
#             if graph[i, j] != -1 and i in valid_S and j in valid_T:
#                 valid_cut += graph[i, j]
#     # print valid cut without process
#     '''
#     print('The valid S cut includes: ')
#     for i in range(len(valid_S)):
#         print(str(valid_S[i] + 1), ', ', end = '')
#     print('\n')
#     print('The valid T cut includes: ')
#     for i in range(len(valid_T)):
#         print(str(valid_T[i] + 1), ', ', end = '')
#     print('\n')
#     print('The valid cut has weight: ', str(valid_cut))
#     '''
#     # get origin cut
#     origin_S = []
#     origin_T = []
#     for i in range(result.x.shape[0]):
#         if result.x[i] >= 0.5:
#             origin_S.append(i)
#         else: 
#             origin_T.append(i)
#     origin_cut = 0
#     for i in range(result.x.shape[0]):
#         for j in range(result.x.shape[0]):
#             if augment_matrix[i, j] != -1 and i in origin_S and j in origin_T:
#                 origin_cut += augment_matrix[i, j]
    

#     return valid_S, valid_T, origin_cut

def update_graph(graph, u, v):
    if verbose:
        print('Edge (' + str(u) + ', ' + str(v) + ') is updated\n')
    graph[u, v] = 0

def main():
    impact_factor, arc_num, vertex_num, core = graph1_parameter()
    # communication_cpu used in scheduling, count the cost of communication in CPU working 
    graph, vertex_cpu, process, communication_cpu = initial_graph_1(vertex_num, arc_num, impact_factor)

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