#!/usr/bin/python3

import time
import foreman
import logging
import requests

URL='http://leinelab.net/ampel/SetStatus.php?status=%s'

if __name__ == '__main__':
    FORMAT= '%(levelname)+8s %(message)s'
    logging.basicConfig(format=FORMAT, level='INFO')
    
    last_status = None
    
    while True:
        status = foreman.notify('Status')

        if last_status != status:
            logging.info('status changed: pushing %s to webserver.' % status)
            requests.get(URL % status)

        last_status = status
        time.sleep(1)
