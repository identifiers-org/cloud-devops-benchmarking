#!/bin/bash
# This is a template script to launch the benchmark
# Author: Manuel Bernal Llinares <mbdebian@gmail.com>

# Get in the application folder
cd app

# Templating
export RESOLVER_HOST=PLACEHOLDER_RESOLVER_HOST
export RESOLVER_PROTOCOL=PLACEHOLDER_RESOLVER_PROTOCOL
export TARGET_RESOLVER_SERVICE_NAME=PLACEHOLDER_TARGET_RESOLVER_SERVICE_NAME
export REQUEST_MODE=PLACEHOLDER_REQUEST_MODE
export BENCHMARK_ORIGIN_NAME=`hostname`

# Activate Python Virtual Environment
source python_install/bin/activate

# Run the benchmark (all the environment variables are set by the calling client)
python scripts/resolver_benchmark.py
