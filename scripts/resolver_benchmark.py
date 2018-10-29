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
import sys
import time
import random
import logging
import requests


# Set logging
# Logging defaults
_logger_formatters = {
    "DEBUG": "%(asctime)s [%(levelname)7s][%(name)18s][%(module)18s, %(lineno)4s] %(message)s",
    "INFO": "%(asctime)s [%(levelname)7s][%(name)18s] %(message)s"
}
_log_level = 'DEBUG'

__log_handlers = []

for llevel, lformat in _logger_formatters.items():
    lhandler = logging.StreamHandler(stream=sys.stdout)
    lhandler.setLevel(getattr(logging, _log_level))
    lformatter = logging.Formatter(_logger_formatters[_log_level])
    lhandler.setFormatter(lformatter)
    __log_handlers.append(lhandler)


def get_log_handlers():
    global __log_handlers
    return __log_handlers


def get_logger_for(self, name):
    """
    Create a logger on demand
    :param name: name to be used in the logger
    :return: a new logger on that name
    """
    lg = logging.getLogger(name)
    for handler in :
        lg.addHandler(handler)
    lg.setLevel(_log_level)
    return lg


logger = get_logger_for('main')


# Environment
resolver_host = os.environ.get('RESOLVER_HOST', 'resolver.api.identifiers.org')
current_region_name = os.environ.get('CURRENT_REGION_NAME', 'EU')


# Helpers
def print_information():
    logger.info("{} INFORMATION {}".format("-" * 20, "-" * 20))
    logger.info("Destination Resolver Host: {}".format(resolver_host))
    logger.info("Current Region Name: {}".format(current_region_name))
    logger.info("{}============={}".format("-" * 20, "-" * 20))


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
