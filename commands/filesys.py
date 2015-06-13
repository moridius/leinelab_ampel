#!/usr/bin/python3

status_file = '/home/leinelab/ampel/commands/status'

# statusStr should be 'Open' or 'Closed'
def SaveStatus(statusStr):
	with open(status_file, 'w') as f:
		f.write(statusStr)

# TODO: what happens if the status file does not exist
def LoadStatus():
	with open(status_file, 'r') as f:
		return f.read()