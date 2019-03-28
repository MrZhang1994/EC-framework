#!/usr/bin/python3
import os
import sys
import subprocess
import random
import resource
from sys import argv
from time import sleep
from datetime import datetime
import shared_lib


def log(file, s):
    file.write('{}: {}\n'.format(datetime.now().__str__(), s))


if __name__ == '__main__':
    try:

        file = open(shared_lib.log_dir, 'w')

        result = os.popen('ls ').read()
        result = result.replace("\n", " ")
        log(file, result)

        result = os.popen('./server local.file1 12345 ').read()
        result = result.replace("\n", " ")
        log(file, result)

        #result = os.popen('ping 172.18.0.2 -c 4 &> ping.log ').read().replace("\n", " ")
        #log(file, result)

        result = os.popen('cat local.file1 ').read()
        result = result.replace("\n", " ")
        log(file, result)

        #result = os.popen('ifconfig').read()
        #log(file, result)

        #result = os.popen('ps -e -orss=').read()
        #result = result.replace("\n", " ")
        #log(file, result)

    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
