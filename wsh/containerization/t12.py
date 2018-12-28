#!/usr/bin/python3

from jsonsocket import JsonServer
from socket import gethostname
from sys import argv
from time import sleep
import resource
from datetime import datetime

def log(file, s):
    file.write('{}: {}\n'.format(datetime.now().__str__(), s))

port = int(argv[2])
RAM = int(argv[3]) * 1024 * 1024
file = open('/root/runtime/t12.log', 'w')
resource.setrlimit(resource.RLIMIT_AS, (RAM, RAM))
try:
    server = JsonServer(gethostname(), port, 4)
    log(file, 'Waiting for input...')
    data = server.serve()
    server.close()
    log(file, 'Received input, closing server')
    sleep_time = int(argv[4])
    if sleep_time != 0:
        log(file, 'Sleeping for {} sec'.format(sleep_time))
        sleep(sleep_time)
        log(file, 'Finish sleeping')
    # left = data[0].get()
    left = data[0]
    log(file, 'Input 1 length: {}'.format(len(left)))
    # right = data[1].get()
    right = data[1]
    log(file, 'Input 2 length: {}'.format(len(right)))
    result = []
    while len(left) != 0 and len(right) != 0:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    if len(left) == 0:
        result += right
    else:
        result += left
    log(file, 'Completed. The length of result is {}'.format(len(result)))
except Exception as e:
    log(file, "Failed: %s" % e)
finally:
    file.close()

