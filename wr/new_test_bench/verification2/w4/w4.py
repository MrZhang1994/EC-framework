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

        result = os.popen('ifconfig && rm -f final.ou*').read()
        log(file, result)

        result = os.popen('./server final.outputfrom2 12348 && ls && chmod 777 final.outputfrom2 && echo "from2 end" >> final.outputfrom2 && date +"%T.%3N" >> final.outputfrom2 ').read()
        log(file, result)

        result = os.popen('./server final.outputfrom3 12347 && ls && chmod 777 final.outputfrom3  && date +"%T.%3N" >> final.outputfrom3 && cat final.outputfrom3 >> final.outputfrom2').read()
        log(file, result)






    except Exception as e:
        log(file, "Failed: {}".format(e))
    finally:
        file.close()
