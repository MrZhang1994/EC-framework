import numpy as np
from scipy.optimize import linprog

graph = np.zeros((12, 12))

def initial_graph():
    for i in range(12):
        for j in range(12):
            graph[i, j] = -1
    graph[0, 1] = 10
    graph[0, 2] = 10
    graph[0, 7] = 10
    graph[1, 2] = 10
    graph[1, 3] = 10
    graph[2, 4] = 10
    graph[2, 5] = 10
    graph[3, 6] = 10
    graph[3, 7] = 10
    graph[4, 8] = 10
    graph[6, 4] = 10
    graph[6, 9] = 10
    graph[7, 9] = 10
    graph[7, 10] = 10
    graph[5, 11] = 0
    graph[8, 11] = 0
    graph[9, 11] = 0
    graph[10, 11] = 0

def update_graph(u, v):
    print('Edge (' + str(u) + ', ' + str(v) + ') is updated\n')
    graph[u, v] = 0

def maxtopcut():
    process = np.array([32, 21, 12, 21, 12, 10, 21, 22, 11, 10, 10, 0])
    core = 2

    vertex_num = graph.shape[0]
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
    flag = 0; 
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

    print('The valid S cut includes: ')
    for i in range(len(valid_S)):
        print(str(valid_S[i] + 1), ', ', end = '')
    print('\n')
    print('The valid T cut includes: ')
    for i in range(len(valid_T)):
        print(str(valid_T[i] + 1), ', ', end = '')
    print('\n')
    print('The valid cut has weight: ', str(valid_cut))
    return valid_S, valid_T, valid_cut




