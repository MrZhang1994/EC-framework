#!/usr/bin/python3

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
        length = 1000
        file = open('/root/runtime/l1_2.log', 'w')
        # pass-in arguments
        host = argv[1]
        port = int(argv[2])
        RAM = int(argv[3]) * 1024 * 1024
        log(file, "Apply memory limit: {} MB".format(RAM / 1024 / 1024))
        resource.setrlimit(resource.RLIMIT_AS, (RAM, RAM))
        sleep_time = int(argv[4])
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
