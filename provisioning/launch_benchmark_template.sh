#!/bin/bash
# This is a template script to launch the benchmark
# Author: Manuel Bernal Llinares <mbdebian@gmail.com>

# Templating
RESOLVER_HOST=PLACEHOLDER_RESOLVER_HOST
RESOLVER_PROTOCOL=PLACEHOLDER_RESOLVER_PROTOCOL
TARGET_RESOLVER_SERVICE_NAME=PLACEHOLDER_TARGET_RESOLVER_SERVICE_NAME
REQUEST_MODE=PLACEHOLDER_REQUEST_MODE
BENCHMARK_ORIGIN_NAME=`hostname`

# Activate Python Virtual Environment
source python_install/bin/activate

# Run the benchmark (all the environment variables are set by the calling client)
python scripts/resolver_benchmark.py
