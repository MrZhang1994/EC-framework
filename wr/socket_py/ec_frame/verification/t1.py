#!/usr/bin/python3
import os
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

if __name__ == '__main__':
    try:
        length = 1000000
        file = open('/root/runtime/t1.log', 'w')

        result = os.popen('echo start ps && ps -e -orss= && echo end ps ').read()
        log(file, result)

        # pass-in arguments
        host = argv[1]
        port = int(argv[2])

        RAM = int(argv[3]) * 1024 * 1024
        log(file, "Apply memory limit: {} MB".format(RAM / 1024 / 1024))
        resource.setrlimit(resource.RLIMIT_AS, (RAM, RAM))

        log(file, "dict  to gen")
        data_to_send = []
        input_data = [random.randint(0, 1000000) for i in range(length)]
        log(file, "dict  to gened")

        result = os.popen('echo start ps && ps -e -orss= && echo end ps').read()
        log(file, result)

        log(file, "Start sorting")
        data_to_send = sorted(input_data)
        log(file, sys.getsizeof(input_data))
        log(file, sys.getsizeof(data_to_send))
        log(file, "End sorting")

        result = os.popen('echo start ps && ps -e -orss= && echo end ps').read()
        log(file, result)


        host = 'worker-2'
        port = 8083
        log(file, "Sending result to {}:{} len:{}".format(host, port,len(data_to_send)))

        client = JsonClient(host, port)
        client.connect()
        client.send_obj(data_to_send, client.socket)
        client.close()

        log(file,'sent 1')

        result = os.popen('echo start ps && ps -e -orss= && echo end ps').read()
        log(file, result)

        host = 'worker-1'
        port = 8082
        log(file, "Sending result to {}:{} len:{}".format(host, port,len(data_to_send)))

        client = JsonClient(host, port)
        client.connect()
        client.send_obj(data_to_send, client.socket)
        client.close()

        log(file,'sent 2')

        log(file, "End sending")

        result = os.popen('echo start ps && ps -e -orss= && echo end ps').read()
        log(file, result)


    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
