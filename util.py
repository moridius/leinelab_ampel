#!/usr/bin/python3

import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))

log_file = None
log_append = False

logger = None

def log(output):
    global log_file, logger

    if logger is None:
        if log_file is not None:
            log_path = script_path + '/' + log_file
            if log_append:
                mode = 'a'
            else:
                mode = 'w'
            logger = open(log_path, mode)
            print('Logging to: ' + log_path)
        else:
            logger = sys.stdout

    logger.write(output + '\n')
    logger.flush()
