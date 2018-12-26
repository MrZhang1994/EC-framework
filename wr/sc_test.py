import numpy as np
import wr_sc

A = [[0, 10, 10, 0, 0, 0, 0, 10, 0, 0, 0, 0.],
     [10, 0, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0.],
     [10, 10, 0, 0, 10, 10, 0, 0, 0, 0, 0, 0.],
     [0, 10, 0, 0, 0, 0, 10, 10, 0, 0, 0, 0.],
     [0, 0, 10, 0, 0, 0, 10, 0, 10, 0, 0, 0.],
     [0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0.],
     [0, 0, 0, 10, 10, 0, 0, 0, 0, 10, 0, 0.],
     [10, 0, 0, 10, 0, 0, 0, 0, 0, 10, 10, 0.],
     [0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 10, 10, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.]]

iso = np.zeros((12, 12), dtype=float)
iso[0][2] = 4
iso[2][0] = 4
iso_threshold = 3

cluster_data, cut_sum = wr_sc.sc(A, iso, iso_threshold)
print(cluster_data)
print(cut_sum)
