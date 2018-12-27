#!/usr/bin/python3

from jsonsocket import JsonServer
from jsonsocket import JsonClient
from socket import gethostname
from sys import argv
from time import sleep
import resource
import random
from datetime import datetime

def log(file, s):
    file.write('{}: {}\n'.format(datetime.now().__str__(), s))

port = int(argv[2])
RAM = int(argv[3]) * 1024 * 1024
file = open('/root/runtime/t9_r.log', 'w')
resource.setrlimit(resource.RLIMIT_AS, (RAM, RAM))
try:
    server = JsonServer(gethostname(), port, 1)
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

if __name__ == '__main__':
    try:
        length = 1000
        file = open('/root/runtime/t9_s.log', 'w')
        # pass-in arguments
        host = argv[1]
        port = int(argv[2])
        RAM = int(argv[3]) * 1024 * 1024
        log(file, "Apply memory limit: {} MB".format(RAM / 1024 / 1024))
        resource.setrlimit(resource.RLIMIT_AS, (RAM, RAM))
        sleep_time = 0
        if sleep_time != 0:
            log(file, "Start sleeping {} sec".format(sleep_time))
            sleep(sleep_time)
            log(file, "Finish sleeping")
        log(file, "Start sorting")
        input_data = [random.randint(0, 100000) for i in range(length)]
        data_to_send = sorted(input_data)
        log(file, "Sending result to {}:{}".format(host, port))
        client = JsonClient(host, port)
        client.connect()
        client.send_obj(data_to_send, client.socket)
        client.close()
    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
