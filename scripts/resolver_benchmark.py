# 
# Project   : cloud-devops-benchmarking
# Timestamp : 26-10-2018 15:34
# Author    : Manuel Bernal Llinares <mbdebian@gmail.com>
# ---
# 

"""
The goal of this script is to create a benchmark report on identifiers.org Resolution API Service
"""

import os
import time
import random
import logging
import requests


# Environment
resolver_host = os.environ.get('RESOLVER_HOST', 'resolver.api.identifiers.org')
current_region_name = os.environ.get('CURRENT_REGION_NAME', 'EU')


# Helpers
def print_information():
    logging.info("{} INFORMATION {}".format("-" * 20, "-" * 20))
    logging.info("Destination Resolver Host: {}".format(resolver_host))
    logging.info("Current Region Name: {}".format(current_region_name))
    logging.info("{}============={}".format("-" * 20, "-" * 20))


def make_rest_request_content_type_json(url):
    # TODO - Magic number here!!!
    n_attempts = 42
    response = None
    while n_attempts:
        n_attempts -= 1
        try:
            response = requests.get(url, headers={"Content-Type": "application/json"})
        except Exception as e:
            # Any possible exception counts towards the attempt counter
            # Random wait - TODO - Another magic number!!!
            time.sleep(random.randint(30))
            continue
        if response.ok:
            return response.json()
        # Random wait - TODO - Another magic number!!!
        time.sleep(random.randint(10))
    response.raise_for_status()


def main():
    print_information()
    # General Algorithm
    # TODO Get resolution dataset
    # TODO Iterate over namespaces requesting the resolver to solve a sample compact identifier within each namespace


if __name__ == '__main__':
    main()
