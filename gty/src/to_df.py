import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

matlab = ["#0073bd", "#d9541a", "#78ab30", "#edb021"]
color_codes_wanted = ['blue', 'red', 'green', 'orange']
c = lambda x: matlab[color_codes_wanted.index(x)]

df = pd.DataFrame(columns=('Type', 'Ratio', 'Times', 'gid', 'k', 'Number of CPU Cores', 'Memory Constraints', 'Isolation Level'))

cores = [2,    3,   4,    5,   6]
mem   = [1, 0.95, 0.9, 0.85,  0.8, 0.75]
isol  = [1.5,  3,   5,  7.5, 10.5]
tests = [[0, 2, 1], [1, 2, 1], [2, 2, 1], [3, 2, 1], [4, 2, 1], [2, 0, 1], [2, 1, 1], [2, 3, 1], [2, 4, 1], [2, 5, 1], [2, 2, 0], [2, 2, 2], [2, 2, 3], [2, 2, 4]]

def draw_read():
    cnt = 0
    for gid in [1, 2, 3, 4]:
        for k in range(14):
            path = './results_heft/graph' + str(gid) + '/' + str(k) + '/'
            
            with open(path+'fb.txt', 'r') as f:
                FB = [float(line.strip()) for line in f.readlines()]

            with open(path+'i2c.txt', 'r') as f:
                I2C = [float(line.strip()) for line in f.readlines()]

            with open(path+'inorder.txt', 'r') as f:
                I = [float(line.strip()) for line in f.readlines()]

            with open(path+'random.txt', 'r') as f:
                R = [float(line.strip()) for line in f.readlines()]

            """
            with open(path+'sc.txt', 'r') as f:
                S = [float(line.strip()) for line in f.readlines()]
            """

            with open(path+'fb_open.txt', 'r') as f:
                FB_open = [float(line.strip()) for line in f.readlines()]

            with open(path+'i2c_open.txt', 'r') as f:
                I2C_open = [float(line.strip()) for line in f.readlines()]

            with open(path+'inorder_open.txt', 'r') as f:
                I_open = [float(line.strip()) for line in f.readlines()]

            with open(path+'random_open.txt', 'r') as f:
                R_open = [float(line.strip()) for line in f.readlines()]

            for i, x in enumerate(FB):
                df.loc[cnt] = ['CPF', x, FB_open[i], gid, k, cores[tests[k][0]], mem[tests[k][1]], isol[tests[k][2]]]
                cnt += 1
            for i, x in enumerate(I2C):
                df.loc[cnt] = ['ICRB', x, I2C_open[i], gid, k, cores[tests[k][0]], mem[tests[k][1]], isol[tests[k][2]]]
                cnt += 1
            for i, x in enumerate(I):
                df.loc[cnt] = ['STO', x, I_open[i], gid, k, cores[tests[k][0]], mem[tests[k][1]], isol[tests[k][2]]]
                cnt += 1
            for i, x in enumerate(R):
                df.loc[cnt] = ['Rand', x, R_open[i], gid, k, cores[tests[k][0]], mem[tests[k][1]], isol[tests[k][2]]]
                cnt += 1
            print(gid, k)
    return 

if __name__ == '__main__':
    draw_read()
    df.to_csv('./df.csv')