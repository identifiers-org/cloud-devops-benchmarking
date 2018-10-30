#!/usr/bin/env bash
# Update and upgrade
sudo apt-get update
sudo apt-get -y upgrade
# Prepare software
sudo apg-get install -y build-essential python3-pip python3-virtualenv virtualenv git
git clone https://github.com/identifiers-org/cloud-devops-benchmarking.git app
cd app
alias pip='pip3'
make install
