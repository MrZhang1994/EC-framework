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
import util

def log(file, s):
    file.write('{}: {}\n'.format(datetime.now().__str__(), s))

if __name__ == '__main__':
    try:
        length = util.length
        file = open('/root/runtime/t1.log', 'w')

        command = util.cmd 

        result = os.popen(command).read()
        log(file, result)

        # pass-in arguments
        host = argv[1]
        port = int(argv[2])

        RAM = int(argv[3]) * 1024 * 1024
        log(file, "Apply memory limit: {} MB".format(RAM / 1024 / 1024))
        resource.setrlimit(resource.RLIMIT_AS, (RAM, RAM))

        log(file, "dict  to gen")
        input_data = [random.randint(0, 1000000) for i in range(length)]
        log(file, "dict  to gened")
        log(file,sys.getsizeof(input_data)) 

        result = os.popen(command).read()
        log(file, result)

        log(file, "Start working")

        util.be_busy()

        sent_data = input_data[0:util.lhed_length]

        log(file, "End working")
        log(file, sys.getsizeof(input_data))

        result = os.popen(command).read()
        log(file, result)


        host = 'worker-2'
        port = 8083
        log(file, "Sending result 1 to {}:{} len:{}".format(host, port,len(input_data)))

        client = JsonClient(host, port)
        client.connect()
        client.send_obj(input_data, client.socket)
        client.close()

        log(file,'After sent 1')

        result = os.popen(command).read()
        log(file, result)

        host = 'worker-1'
        port = 8082
        log(file, "Start Sending 2 result to {}:{} len:{}".format(host, port,len(sent_data)))

        client = JsonClient(host, port)
        client.connect()
        client.send_obj(sent_data, client.socket)
        client.close()

        log(file,'After sent 2')

        log(file, "End sending")

        result = os.popen(command).read()
        log(file, result)


    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
