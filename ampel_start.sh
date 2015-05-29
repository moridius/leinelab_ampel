#!/bin/bash

# Set PYTHONPATH so the script can find Twython
#export PYTHONPATH=/home/leinelab/ampel/ve/lib/python3.2/site-packages/
export PYTHONPATH=/home/leinelab/ampel/ve3/lib/python3.2/site-packages/

# Activate virtualenv
#source /home/leinelab/ampel/ve/bin/activate
source /home/leinelab/ampel/ve3/bin/activate

echo "Starte Ampel-Skript..."

# Start Ampel
/home/leinelab/ampel/foreman.py 2>&1 | tee /home/leinelab/ampel/ampel.log
#/home/leinelab/ampel/foreman.py
