#!/bin/bash
folder_script_home=$(dirname "$0")
folder_reports='reports'
regions=( europe-west4 us-central1 australia-southeast1 asia-east1 asia-northeast1 asia-south1 )
vm_name_prefix='resolver-benchmarkvm'

# Logging subsystem
source "${folder_script_home}"/tinylogger.bash

# Set the logging level
LOGGER_LVL=debug

for region in "${regions[@]}"; do
    zone="${region}-a"
    vm_name="${vm_name_prefix}-${region}"
    echo "---> Region: ${region}"
    echo -e "\tZone  : ${zone}"
    echo -e "\tVM    : ${vm_name}"
done
