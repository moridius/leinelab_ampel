#!/usr/bin/python3

import requests
import time
import argparse
import foreman
import logging

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-level', type=str, default='INFO',
                        dest='log_level')

    args = parser.parse_args()

    FORMAT = '%(levelname)+8s %(message)s'
    logging.basicConfig(format=FORMAT, level=args.log_level)

    while True:
        res = requests.get("http://leinelab.net/ampel/GetJob.php")
        content = res.text

        if content != "":
            foreman.notify(content)
            logging.info("Polled webserver and got something.")
        else:
            logging.debug("Polled webserver, got nothing.")

        time.sleep(15)
