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
import numpy as np
import pandas as pd
from scipy import stats
# App imports
from models import ResponseTimeEntry, ResponseTimeDataset


# Set logging
# Logging defaults
_logger_formatters = {
    "DEBUG": "%(asctime)s [%(levelname)7s][%(name)10s][%(module)18s, %(lineno)4s] %(message)s",
    "INFO": "%(asctime)s [%(levelname)7s][%(name)10s] %(message)s"
}
_log_level = os.environ.get('LOGLEVEL', 'INFO')
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
resolver_protocol = os.environ.get('RESOLVER_PROTOCOL', 'http')
current_region_name = os.environ.get('CURRENT_REGION_NAME', 'EU')
target_resolver_service_name = os.environ.get("TARGET_RESOLVER_SERVICE_NAME", 'cloud')
hq_registry_host = os.environ.get('HQ_REGISTRY_HOST', 'registry.api.hq.identifiers.org')
hq_registry_protocol = os.environ.get('HQ_REGISTRY_PROTOCOL', 'http')
request_mode = os.environ.get('REQUEST_MODE', 'api')
benchmark_origin_name = os.environ.get('BENCHMARK_ORIGIN_NAME', 'laptop_ebi')


# To be externalized
def get_reports_folder():
    return "reports"


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
# Response Time Dataset
RESPONSE_TIME_DATASET_KEY_URL = 'url'
RESPONSE_TIME_DATASET_KEY_STATUS = 'status'
RESPONSE_TIME_DATASET_KEY_ERROR = 'error'
RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME = 'Response_Time(ms)'
RESPONSE_TIME_DATASET_VALUE_STATUS_ERROR = 'ERROR'
RESPONSE_TIME_DATASET_VALUE_STATUS_OK = 'OK'


# Globals
__resolution_endpoint = None
__hq_registry_resolution_dataset_endpoint = None


# Helpers
current_time_millis = lambda: int(round(time.time() * 1000))


def print_information():
    logger.info("{} INFORMATION {}".format("-" * 20, "-" * 20))
    logger.info("Destination Resolver Host: {}".format(resolver_host))
    logger.info("Current Region Name: {}".format(current_region_name))
    logger.info("Benchmark Origin: {}".format(benchmark_origin_name))
    logger.info("Destination Deployment: {}".format(target_resolver_service_name))
    logger.info("{}============={}".format("-" * 20, "-" * 20))


def get_resolution_endpoint():
    global __resolution_endpoint
    if __resolution_endpoint is None:
        __resolution_endpoint = "{}://{}".format(resolver_protocol, resolver_host)
    return __resolution_endpoint


def get_hq_registry_resolution_dataset_endpoint():
    global __hq_registry_resolution_dataset_endpoint
    if __hq_registry_resolution_dataset_endpoint is None:
        __hq_registry_resolution_dataset_endpoint = "{}://{}/resolutionApi/getResolverDataset".format(hq_registry_protocol, hq_registry_host)
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


def make_unique_rest_request_content_type_json(url):
    response = None
    try:
        response = requests.get(url, headers={"Content-Type": "application/json"})
    except Exception as e:
        logger.error("EXCEPTION on request URL '{}', '{}'".format(url, e))
    if response.ok:
        return response.json()
    response.raise_for_status()


def make_unique_http_get_request(url):
    response = None
    try:
        response = requests.get(url, allow_redirects=False)
    except Exception as e:
        logger.error("EXCEPTION on request URL '{}', '{}'".format(url, e))
    if response.ok:
        return response
    response.raise_for_status()


def grow_dataset(dataset, nfinal=1000000):
    grown_dataset = []
    if nfinal < len(dataset):
        nfinal = len(dataset)
    grown_dataset = np.append(grown_dataset, dataset)
    logger.info("Growing initial dataset of #{} elements up to #{} elements".format(len(dataset), nfinal))
    while len(grown_dataset) < nfinal:
        growth_size = min(len(grown_dataset), nfinal - len(grown_dataset))
        logger.debug("Growth step, +{} items".format(growth_size))
        grown_dataset = np.append(grown_dataset, dataset[: growth_size])
    logger.info("Shuffling grown dataset of #{} items".format(len(grown_dataset)))
    random.shuffle(grown_dataset)
    return grown_dataset


def get_compact_identifiers_dataset():
    # Get resolution dataset
    response = make_rest_request_content_type_json(get_hq_registry_resolution_dataset_endpoint())
    resolution_dataset = []
    if HQ_RESPONSE_KEY_PAYLOAD in response and HQ_RESPONSE_KEY_PAYLOAD_NAMESPACES in response[HQ_RESPONSE_KEY_PAYLOAD]:
        resolution_dataset = response[HQ_RESPONSE_KEY_PAYLOAD][HQ_RESPONSE_KEY_PAYLOAD_NAMESPACES]
    logger.info("Building Compact Identifiers for #{} namespaces".format(len(resolution_dataset)))
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


def get_response_times_for_compact_identifiers(compact_identifiers):
    logger.info("Measuring Response Times for #{} Compact Identifiers".format(len(compact_identifiers)))
    response_times_dataset = ResponseTimeDataset()
    response_times_stats = {}
    response_times = []
    for index, compact_identifier in enumerate(compact_identifiers):
        query_url = "{}/{}".format(get_resolution_endpoint(), compact_identifier)
        response_times_stats[index] = {}
        response_times_stats[index][RESPONSE_TIME_DATASET_KEY_URL] = query_url
        response_time_entry = ResponseTimeEntry(url=query_url)
        start_time = current_time_millis()
        try:
            if request_mode == 'api':
                response = make_unique_rest_request_content_type_json(query_url)
            else:
                response = make_unique_http_get_request(query_url)
        except Exception as e:
            logger.error("ERROR measuring response time for URL '{}', error '{}'".format(query_url, e))
            response_times_stats[index][RESPONSE_TIME_DATASET_KEY_STATUS] = RESPONSE_TIME_DATASET_VALUE_STATUS_ERROR
            response_times_stats[index][RESPONSE_TIME_DATASET_KEY_ERROR] = "{}".format(e)
            response_time_entry.error = "{}".format(e)
            response_time_entry.status = ResponseTimeDataset.RESPONSE_TIME_DATASET_VALUE_STATUS_ERROR
            response_times_dataset.add_entry(response_time_entry)
            continue
        response_times_stats[index][RESPONSE_TIME_DATASET_KEY_STATUS] = RESPONSE_TIME_DATASET_VALUE_STATUS_OK
        stop_time = current_time_millis()
        delta_time = stop_time - start_time
        response_times_stats[index][RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME] = delta_time
        response_times.append(delta_time)
        response_time_entry.status = ResponseTimeDataset.RESPONSE_TIME_DATASET_VALUE_STATUS_OK
        response_time_entry.response_time = delta_time
        response_times_dataset.add_entry(response_time_entry)
    return response_times, response_times_dataset


def present_response_times_stats(response_times_dataset):
    success_rate = response_times_dataset.get_number_success_entries() * 100.0 / response_times_dataset.get_number_of_entries();
    error_rate = response_times_dataset.get_number_error_entries() * 100.0 / response_times_dataset.get_number_of_entries();
    logger.info("--- Response Times Stats ---")
    logger.info("Number of tests: #{}".format(response_times_dataset.get_number_of_entries()))
    logger.info("Successful tests: #{} ({:.2f}%)".format(response_times_dataset.get_number_success_entries(), success_rate))
    logger.info("ERROR Rate: {:.2f}%".format(error_rate))
    logger.info("Mean response time: {:.2f}".format(response_times_dataset.get_response_time_arithmetic_mean()))
    logger.info("Mode response time: {}".format(response_times_dataset.get_response_time_mode()[0]))
    logger.info("Median response time: {}".format(response_times_dataset.get_response_time_median()))
    logger.info("Standard Deviation response time: {:.2f}".format(response_times_dataset.get_response_time_standard_deviation()))
    logger.info("----------------------------")


def main():
    print_information()
    # Get resolution dataset
    compact_identifiers = get_compact_identifiers_dataset()
    # Measure response time
    response_times, response_times_dataset = get_response_times_for_compact_identifiers(grow_dataset(compact_identifiers, 1000))
    print("Response Times description:\n{}".format(stats.describe(response_times)))
    # Print Response times statistics
    present_response_times_stats(response_times_dataset)
    # Dump response times stats
    file_prefix = "{}-to-{}_at_{}".format(benchmark_origin_name, target_resolver_service_name, current_region_name)
    file_response_times_dataset = os.path.join(get_reports_folder(), "{}-response_times_dataset.csv".format(file_prefix))
    logger.info("Dumping response times dataset to file '{}'".format(file_response_times_dataset))
    response_times_dataset.to_csv(file_response_times_dataset)
    file_response_times_stats = os.path.join(get_reports_folder(), "{}-response_times_stats.csv".format(file_prefix))
    logger.info("Dumping response times stats to file '{}'".format(file_response_times_stats))
    response_times_dataset.stats_to_csv(file_response_times_stats)
    with open(os.path.join(get_reports_folder(), "done.flag"), 'w') as f:
        f.write("Done!")


if __name__ == '__main__':
    main()
