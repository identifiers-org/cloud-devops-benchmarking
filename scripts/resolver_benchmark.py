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
    "DEBUG": "%(asctime)s [%(levelname)7s][%(name)10s][%(module)18s, %(lineno)4s] %(message)s",
    "INFO": "%(asctime)s [%(levelname)7s][%(name)10s] %(message)s"
}
_log_level = 'DEBUG'
# In case I want multiple handlers
__log_handlers = []

lformat = _logger_formatters[_log_level]
lhandler = logging.StreamHandler(stream=sys.stdout)
lhandler.setLevel(getattr(logging, _log_level))
lformatter = logging.Formatter(_logger_formatters[_log_level])
lhandler.setFormatter(lformatter)
__log_handlers.append(lhandler)


def get_log_handlers():
    global __log_handlers
    return __log_handlers


def get_logger_for(name):
    """
    Create a logger on demand
    :param name: name to be used in the logger
    :return: a new logger on that name
    """
    lg = logging.getLogger(name)
    for handler in get_log_handlers():
        lg.addHandler(handler)
    lg.setLevel(_log_level)
    return lg


logger = get_logger_for('main')


# Environment
resolver_host = os.environ.get('RESOLVER_HOST', 'resolver.api.identifiers.org')
resolver_protocol = os.environ.get('PROTOCOL', 'http')
current_region_name = os.environ.get('CURRENT_REGION_NAME', 'EU')
hq_registry_host = os.environ.get('HQ_REGISTRY_HOST', 'registry.api.hq.identifiers.org')
hq_registry_protocol = os.environ.get('HQ_REGISTRY_PROTOCOL', 'http')


# Constants
# Resolution Source Data Model
HQ_RESPONSE_KEY_PAYLOAD = 'payload'
HQ_RESPONSE_KEY_PAYLOAD_NAMESPACES = 'namespaces'
PID_ENTRY_KEY_ID = 'id'
PID_ENTRY_KEY_NAME = 'name'
PID_ENTRY_KEY_PATTERN = 'pattern'
PID_ENTRY_KEY_DEFINITION = 'definition'
PID_ENTRY_KEY_PREFIX = 'prefix'
PID_ENTRY_KEY_URL = 'url'
PID_ENTRY_KEY_PREFIXED = 'prefixed'
PID_ENTRY_KEY_RESOURCES = 'resources'
RESOURCE_ENTRY_KEY_ID = 'id'
RESOURCE_ENTRY_KEY_ACCESS_URL = 'accessURL'
RESOURCE_ENTRY_KEY_INFO = 'info'
RESOURCE_ENTRY_KEY_INSTITUTION = 'institution'
RESOURCE_ENTRY_KEY_LOCATION = 'location'
RESOURCE_ENTRY_KEY_OFFICIAL = 'official'
RESOURCE_ENTRY_KEY_RESOURCE_PREFIX = 'resourcePrefix'
RESOURCE_ENTRY_KEY_LOCAL_ID = 'localId'
RESOURCE_ENTRY_KEY_TEST_STRING = 'testString'
RESOURCE_ENTRY_KEY_RESOURCE_URL = 'resourceURL'


# Globals
__resolution_endpoint = None
__hq_registry_resolution_dataset_endpoint = None


# Helpers
def print_information():
    logger.info("{} INFORMATION {}".format("-" * 20, "-" * 20))
    logger.info("Destination Resolver Host: {}".format(resolver_host))
    logger.info("Current Region Name: {}".format(current_region_name))
    logger.info("{}============={}".format("-" * 20, "-" * 20))


def get_resolution_endpoint():
    global __resolution_endpoint
    if __resolution_endpoint is None:
        __resolution_endpoint = "{}://{}/".format(resolver_protocol, resolver_host)
    return __resolution_endpoint


def get_hq_registry_resolution_dataset_endpoint():
    global __hq_registry_resolution_dataset_endpoint
    if __hq_registry_resolution_dataset_endpoint is None:
        __hq_registry_resolution_dataset_endpoint = "{}://{}/resolutionApi/getResolverDataset"
    return __hq_registry_resolution_dataset_endpoint


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


def get_compact_identifiers_dataset():
    # Get resolution dataset
    response = make_rest_request_content_type_json(get_hq_registry_resolution_dataset_endpoint())
    resolution_dataset = []
    if HQ_RESPONSE_KEY_PAYLOAD in response and HQ_RESPONSE_KEY_PAYLOAD_NAMESPACES in response[HQ_RESPONSE_KEY_PAYLOAD]:
        resolution_dataset = response[HQ_RESPONSE_KEY_PAYLOAD][HQ_RESPONSE_KEY_PAYLOAD_NAMESPACES]
    logger.debug("Building Compact Identifiers for #{} namespaces".format(len(resolution_dataset)))
    compact_identifiers = []
    for namespace in resolution_dataset:
        if PID_ENTRY_KEY_PREFIX not in namespace or namespace[PID_ENTRY_KEY_PREFIX] is None:
            logger.error("SKIPPING Namespace '{}', NO PREFIX FOUND".format(namespace[PID_ENTRY_KEY_ID]))
            continue
        if PID_ENTRY_KEY_RESOURCES not in namespace or namespace[PID_ENTRY_KEY_RESOURCES] is None:
            logger.error("SKIPPING Namespace '{}', NO RESOURCES FOUND".format(namespace[PID_ENTRY_KEY_ID]))
            continue
        sample_id = None
        for resource in namespace[PID_ENTRY_KEY_RESOURCES]:
            if RESOURCE_ENTRY_KEY_LOCAL_ID not in resource or resource[RESOURCE_ENTRY_KEY_LOCAL_ID] is None:
                logger.error("SKIPPING Resource '{}', it has NO LOCAL ID".format(resource[RESOURCE_ENTRY_KEY_ID]))
                continue
            sample_id = resource[RESOURCE_ENTRY_KEY_LOCAL_ID]
            # We just need one local ID
            break
        if sample_id is None:
            logger.error("SKIPPING Namespace '{}', NO RESOURCES WITH LOCAL ID FOUND".format(namespace[PID_ENTRY_KEY_ID]))
            continue
        compact_identifier = "{}:{}".format(namespace[PID_ENTRY_KEY_PREFIX], sample_id)
        logger.debug("Compact Identifier '{}' added to the dataset".format(compact_identifier))
        compact_identifiers.append(compact_identifier)
    return compact_identifiers


def main():
    print_information()
    compact_identifiers = get_compact_identifiers_dataset()
    # General Algorithm
    # TODO Get resolution dataset
    # TODO Iterate over namespaces requesting the resolver to solve a sample compact identifier within each namespace


if __name__ == '__main__':
    main()
