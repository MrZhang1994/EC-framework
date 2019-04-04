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


        result = os.popen('./client images_to_send.zip 172.18.0.3 12345').read()
        result = result.replace("\n", " ")
        log(file, result)


        #result = os.popen('./client images_to_send.zip 172.18.0.3 12345 ').read()
        #result = result.replace("\n", " ")
        #log(file, result)

        result = os.popen('ps -e -orss=').read()
        result = result.replace("\n", " ")
        log(file, result)

    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
