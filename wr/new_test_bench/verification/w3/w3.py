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

        result = os.popen('./server got.zip 12346').read()
        log(file, result)

        result = os.popen('ls').read()
        log(file, result)

        result = os.popen('unzip got.zip ').read()
        log(file, result)

        result = os.popen('python2 train-license-digits.py predict > predict_result.txt').read()
        result = result.replace("\n", " ")
        log(file, result)

    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
