#!/bin/bash
folder_script_home=$(dirname "$0")
folder_reports=${PROVISIONING_FOLDER_REPORTS:='reports'}
folder_tmp=${PROVISIONING_FOLDER_TMP:='tmp'}
pending_zones=( us-central1 australia-southeast1 asia-east1 asia-northeast1 asia-south1 )
regions=( europe-west4 )
vm_name_prefix='resolver-benchmarkvm'
vm_script_init="${folder_script_home}"/vminit.sh
vm_script_app_install="${folder_script_home}"/install_benchmark_app.sh
vm_script_run_benchmark_template="${folder_script_home}"/launch_benchmark_template.sh

# Logging subsystem
source "${folder_script_home}"/tinylogger.bash

# Set the logging level
LOGGER_LVL=debug

created_vms_and_zones=( )
created_vms_and_ips=( )
for region in "${regions[@]}"; do
    zone="${region}-a"
    vm_name="${vm_name_prefix}-${region}"
    echo "---> Region: ${region}"
    echo -e "\tZone  : ${zone}"
    echo -e "\tVM    : ${vm_name}"
    echo -e "\tLaunching VM..."
    gcloud -q compute --project=${google_cloud_project} instances create ${vm_name} --zone=${zone} --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=${google_cloud_service_account} --scopes=https://www.googleapis.com/auth/cloud-platform --image=debian-9-stretch-v20181011 --image-project=debian-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=${vm_name} --labels=app=resolver-benchmark,region=${region}
    vm_external_ip=`gcloud compute instances list --filter=${vm_name} --format=yaml | grep natIP | cut -f2 -d':' | awk '{$1=$1;print}'`
    echo -e "\tVM External IP: ${vm_external_ip}"
    ssh-keygen -R ${vm_external_ip}
    created_vms_and_zones=( ["${vm_name}"]="${zone}" "${created_vms_and_zones[@]}" )
    created_vms_and_ips=( ["${vm_name}"]="${vm_external_ip}" "${created_vms_and_ips[@]}" )
done
