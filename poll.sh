#!/bin/bash

export PYTHONPATH=/home/leinelab/ampel/ve3/lib/python3.2/site-packages/
source /home/leinelab/ampel/ve3/bin/activate

/home/leinelab/ampel/poll_webserver.py 2>&1 | tee /home/leinelab/ampel/poll.log
