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

        result = os.popen('rm -rf test_images').read()
        result = os.popen('rm -rf image_to_send').read()
        result = os.popen('rm -rf sig').read()
        result = os.popen('rm -rf car').read()

        result = os.popen('./server got.zip 12345').read()
        log(file, result)

        #result = os.popen('./server got.zip 12345').read()
        #log(file, result)

        result = os.popen('ls ').read()
        log(file, result)

        result = os.popen('unzip got.zip ').read()
        log(file, result)
        result = os.popen('mv images_to_send test_images').read()
        log(file, result)

        result = os.popen('echo try cding').read();
        log(file, result)

        result = os.popen('ls').read()
        log(file, result)

        result = os.popen('cd darknet && ls && ./darknet classifier predict cfg/imagenet1k.data cfg/darknet.cfg darknet.weights ../test_images/img_sig.jpg > ../sig.output').read()
        log(file, result)
        result = os.popen('cd darknet && ls && ./darknet classifier predict cfg/imagenet1k.data cfg/darknet.cfg darknet.weights ../test_images/img_car.jpg > ../car.output').read()
        log(file, result)
        result = os.popen('cd darknet && ls && ./darknet classifier predict cfg/imagenet1k.data cfg/darknet.cfg darknet.weights ../test_images/img_human.jpg > ../human.output').read()
        log(file, result)

        result = os.popen('cat car.output > total.output && cat human.output >> total.output && cat sig.output >> total.output').read()
        log(file, result)

        """result = os.popen('unzip got1.zip ').read()
        log(file, result)
        result = os.popen('mv images_to_send sig').read()
        log(file, result)

        result = os.popen('unzip got2.zip ').read()
        log(file, result)
        result = os.popen('mv images_to_send car').read()
        log(file, result) """

        result = os.popen('python2 train-license-digits.py predict > predict_result.txt').read()
        result = result.replace("\n", " ")
        log(file, result)

    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
