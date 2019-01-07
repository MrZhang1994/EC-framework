#!/usr/bin/python3
import os
from jsonsocket import JsonServer
from socket import gethostname
from sys import argv
from time import sleep
import resource
from datetime import datetime
import sys
import subprocess
from jsonsocket import JsonClient
import random
import resource
from sys import argv
from time import sleep
from datetime import datetime


def log(file, s):
    file.write('{}: {}\n'.format(datetime.now().__str__(), s))


port = int(argv[2])
RAM = int(argv[3]) * 1024 * 1024
file = open('/root/runtime/t3.log', 'w')
resource.setrlimit(resource.RLIMIT_AS, (RAM, RAM))
try:
    result = os.popen('echo start ps && ps -e -orss= && echo end ps ').read()
    log(file, result)

    port = 8083
    server = JsonServer(gethostname(), port, 1)
    log(file, 'Waiting for input...')

    data = server.serve()
    server.close()
    log(file, 'Received input, closing server')

    result = os.popen('echo start ps && ps -e -orss= && echo end ps ').read()
    log(file, result)


    left = data[0]
    log(file, 'Input 1 length: {}'.format(len(left)))
    # right = data[1].get()
    result = []
    # while len(left) != 0 and len(right) != 0:
    #     if left[0] <= right[0]:
    #         result.append(left.pop(0))
    #     else:
    #         result.append(right.pop(0))
    # if len(left) == 0:
    #     result += right
    # else:
    #     result += left
    result += left
    log(file, 'Completed. The length of result is {}'.format(len(result)))

    length = 1000000

    data_to_send = []
    input_data = [random.randint(0, 1000000) for i in range(length)]
    log(file, 'Random gened')

    result = os.popen('echo start ps && ps -e -orss= && echo end ps ').read()
    log(file, result)

    data_to_send = sorted(input_data)
    log(file, 'sorted')

    result = os.popen('echo start ps && ps -e -orss= && echo end ps ').read()
    log(file, result)

    host = 'worker-2'
    port = 8084
    log(file, "Sending result to {}:{}".format(host, port))
    client = JsonClient(host, port)
    client.connect()
    client.send_obj(data_to_send, client.socket)
    client.close()
    log(file, "end sending to {}:{}".format(host, port))

    log(file, 'sent')

    result = os.popen('echo start ps && ps -e -orss= && echo end ps ').read()
    log(file, result)


except Exception as e:
    log(file, "Failed: %s" % e)
finally:
    file.close()
