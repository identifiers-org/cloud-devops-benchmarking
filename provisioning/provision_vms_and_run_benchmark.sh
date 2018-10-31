#!/bin/bash
folder_script_home=$(dirname "$0")
folder_reports='reports'
pending_zones=( us-central1 australia-southeast1 asia-east1 asia-northeast1 asia-south1 )
regions=( europe-west4 )
vm_name_prefix='resolver-benchmarkvm'
vm_init_script="${folder_script_home}"/vminit.sh

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
