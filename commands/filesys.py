#!/usr/bin/python3

status_file = '/home/leinelab/ampel/commands/status'

# statusStr should be 'Open' or 'Closed'
def SaveStatus(statusStr):
	with open(status_file, 'w') as f:
		f.write(statusStr)