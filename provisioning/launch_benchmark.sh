#!/bin/bash
# Update and upgrade
sudo apt-get update
sudo apt-get -y upgrade
# Prepare software
sudo apt-get install -y build-essential python3-pip python3-virtualenv virtualenv git
git clone https://github.com/identifiers-org/cloud-devops-benchmarking.git app
cd app
alias pip='pip3'
make install
# Run the benchmark (all the environment variables are set by the calling client)
#export RESOLVER_HOST=identifiers.org; export RESOLVER_PROTOCOL=https; export TARGET_RESOLVER_SERVICE_NAME=ebi; export REQUEST_MODE=noapi; export BENCHMARK_ORIGIN_NAME=`hostname`; python scripts/resolver_benchmark.py
# Activate Python virtual environment
source python_install/bin/activate
python scripts/resolver_benchmark.py
