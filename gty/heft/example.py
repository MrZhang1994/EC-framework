"""
This is a simple script to use the HEFT function provided based on the example given in the original HEFT paper.
You have to define the DAG, compcost function and commcost funtion.

Each task/job is numbered 1 to 10
Each processor/agent is named 'a', 'b' and 'c'

Output expected:
Ranking:
[10, 8, 7, 9, 6, 5, 2, 4, 3, 1]
Schedule:
('a', [Event(job=2, start=27, end=40), Event(job=8, start=57, end=62)])
('b', [Event(job=4, start=18, end=26), Event(job=6, start=26, end=42), Event(job=9, start=56, end=68), Event(job=10, start=73, end=80)])
('c', [Event(job=1, start=0, end=9), Event(job=3, start=9, end=28), Event(job=5, start=28, end=38), Event(job=7, start=38, end=49)])
{1: 'c', 2: 'a', 3: 'c', 4: 'b', 5: 'c', 6: 'b', 7: 'c', 8: 'a', 9: 'b', 10: 'b'}
"""

'''
dag={1:(2,3,4,5,6),
     2:(8,9),
     3:(7,),
     4:(8,9),
     5:(9,),
     6:(8,),
     7:(10,),
     8:(10,),
     9:(10,),
     10:()}
     17.0, 19.0, 17.0, 16.0, 12.0, 17.0, 12.0, 20.0, 8.0, 17.0, 7.0, 7.0
'''
dag={1:(2,3,8),
     2:(3,4),
     3:(5,6),
     4:(7,8),
     5:(9,),
     6:(12,),
     7:(5,10),
     8:(10,11),
     9:(12,),
     10:(12,),
     11:(12,),
     12:()}

def compcost(job, agent):
    if(job==0):
        return 0
    if(job==1):
        return 42
    if(job==2):
        return 94
    if(job==3):
        return 105
    if(job==4):
        return 112
    if(job==5):
        return 44
    if(job==6):
        return 58
    if(job==7):
        return 109
    if(job==8):
        return 64
    if(job==9):
        return 42
    if(job==10):
        return 68
    if(job==11):
        return 44
    if(job==12):
        return 30


def commcost(ni, nj, A, B):
    return 0

    if(A==B):
        return 0
    else:
        if(ni==1 and nj==2):
            return 3
        if(ni==1 and nj==3):
            return 2
        if(ni==1 and nj==8):
            return 7
        if(ni==2 and nj==3):
            return 6
        if(ni==2 and nj==4):
            return 8
        if(ni==3 and nj==5):
            return 6
        if(ni==3 and nj==6):
            return 9
        if(ni==4 and nj==7):
            return 5
        if(ni==4 and nj==8):
            return 7
        if(ni==5 and nj==9):
            return 4
        if(ni==7 and nj==5):
            return 5
        if(ni==7 and nj==10):
            return 4
        if(ni==8 and nj==10):
            return 8
        if(ni==8 and nj==11):
            return 6
        if(ni==6 and nj==12):
            return 8
        if(ni==9 and nj==12):
            return 2
        if(ni==10 and nj==12):
            return 8
        if(ni==11 and nj==12):
            return 4
        else:
            return 0

def commcost_con(ni, nj):
    if(ni==1 and nj==2):
        return 3
    if(ni==1 and nj==3):
        return 2
    if(ni==1 and nj==8):
        return 7
    if(ni==2 and nj==3):
        return 6
    if(ni==2 and nj==4):
        return 8
    if(ni==3 and nj==5):
        return 6
    if(ni==3 and nj==6):
        return 9
    if(ni==4 and nj==7):
        return 5
    if(ni==4 and nj==8):
        return 7
    if(ni==5 and nj==9):
        return 4
    if(ni==7 and nj==5):
        return 5
    if(ni==7 and nj==10):
        return 4
    if(ni==8 and nj==10):
        return 8
    if(ni==8 and nj==11):
        return 6
    if(ni==6 and nj==12):
        return 8
    if(ni==9 and nj==12):
        return 2
    if(ni==10 and nj==12):
        return 8
    if(ni==11 and nj==12):
        return 4
    else:
        return 0