import numpy as np
import wr_sc

A = [[0, 10, 10, 0, 0, 0, 0, 10, 0, 0, 0, 0.],
     [0, 0, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0.],
     [0, 0, 0, 0, 10, 10, 0, 0, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 10, 10, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 10, 0, 10, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0.],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0.],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.]]

iso = np.zeros((12, 12), dtype=float)
iso[0][3] = 4
iso_threshold = 3

import time

start = time.time()


time_ma = [0]
for i in range(10):
    cluster_data, cut_sum = wr_sc.sc(A, iso, iso_threshold, time_ma)

end = time.time()
print(end - start)
print(time_ma[0])
