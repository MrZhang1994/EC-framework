cmd = 'echo start ps && ps -e -orss,args= && echo end ps'


def be_busy():
    for i in range(int(10000/3*5)):
        for j in range(1000):
            a = 1+1
