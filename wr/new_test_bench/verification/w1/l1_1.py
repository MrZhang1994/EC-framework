#!/usr/bin/python3
import os
import sys
import subprocess
import random
import resource
from sys import argv
from time import sleep
from datetime import datetime

def log(file, s):
    file.write('{}: {}\n'.format(datetime.now().__str__(), s))

if __name__ == '__main__':
    try:

        file = open('/root/runtime/l1_1.log', 'w')

        result = os.popen('ls runtime').read()
        result = result.replace("\n", " ")
        log(file, result)

        result = os.popen('ps -e -orss=').read()
        result = result.replace("\n", " ")
        log(file, result)

        a = 0
        while a < 1000000:
            a = a + 1
        log(file, a)


    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
