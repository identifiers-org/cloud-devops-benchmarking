#!/bin/bash
# This is the initialization script for the VM itself, to prepare all the environment for running the benchmarks
# Author: Manuel Bernal Llinares <mbdebian@gmail.com>

# Update and upgrade
sudo apt-get update
sudo apt-get -y upgrade
# Prepare software
sudo apt-get install -y build-essential python3-pip python3-virtualenv virtualenv git
