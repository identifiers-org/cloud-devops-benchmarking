#!/bin/bash
# This is a template script to launch the benchmark
# Author: Manuel Bernal Llinares <mbdebian@gmail.com>

# Templating
RESOLVER_HOST=identifiers.org
RESOLVER_PROTOCOL=https
TARGET_RESOLVER_SERVICE_NAME=ebi
REQUEST_MODE=noapi
BENCHMARK_ORIGIN_NAME=`hostname`

# Activate Python Virtual Environment
source python_install/bin/activate

# Run the benchmark (all the environment variables are set by the calling client)
python scripts/resolver_benchmark.py
