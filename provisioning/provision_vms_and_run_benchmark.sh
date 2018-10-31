#!/bin/bash
# DISCLAIMER: yes, I know this code sucks, but I needed these numbers as soon as possible, I cannot be stuck on this. Also, it
# served its purpose as a way of getting to know better Terraform
folder_script_home=$(dirname "$0")
folder_reports=${PROVISIONING_FOLDER_REPORTS:='reports'}
folder_tmp=${PROVISIONING_FOLDER_TMP:='tmp'}
pending_zones=( us-central1 australia-southeast1 asia-east1 asia-northeast1 asia-south1 )
regions=( europe-west4 )
vm_name_prefix='resolver-benchmarkvm'
vm_script_init="${folder_script_home}"/vminit.sh
vm_script_app_install="${folder_script_home}"/install_benchmark_app.sh
vm_script_run_benchmark_template="${folder_script_home}"/launch_benchmark_template.sh
# THE FOLLOWING ARE NEEDED FROM ENVIRONMENT
google_cloud_project=${PROVISIONING_GOOGLE_CLOUD_PROJECT:='not_provided'}
google_cloud_service_account=${PROVISIONING_GOOGLE_CLOUD_SERVICE_ACCOUNT:='not_provided'}

# TODO - Check the needed variables

# Logging subsystem
source "${folder_script_home}"/tinylogger.bash

# Set the logging level
LOGGER_LVL=debug

# Buck you shell scripting! no idea how to build these associative arrays
declare -a created_vms_and_zones
declare -a created_vms_and_ips
created_vms=( )
for region in "${regions[@]}"; do
    zone="${region}-a"
    vm_name="${vm_name_prefix}-${region}"
    echo "---> Region: ${region}"
    echo -e "\tZone  : ${zone}"
    echo -e "\tVM    : ${vm_name}"
    echo -e "\tLaunching VM..."
    #gcloud -q compute --project=${google_cloud_project} instances create ${vm_name} --zone=${zone} --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=${google_cloud_service_account} --scopes=https://www.googleapis.com/auth/cloud-platform --image=debian-9-stretch-v20181011 --image-project=debian-cloud --boot-disk-size=10GB --boot-disk-type=pd-standard --boot-disk-device-name=${vm_name} --labels=app=resolver-benchmark,region=${region}
    vm_external_ip=`gcloud compute instances list --filter=${vm_name} --format=yaml | grep natIP | cut -f2 -d':' | awk '{$1=$1;print}'`
    echo -e "\tVM External IP: ${vm_external_ip}"
    created_vms_and_zones["${vm_name}"]="${zone}"
    created_vms_and_ips["${vm_name}"]="${vm_external_ip}"
    created_vms+="${vm_name}"
    ssh-keygen -R ${vm_external_ip}
    echo -e "\tInit VM... (${vm_script_init})"
    #scp -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" "${vm_script_init}" ${vm_external_ip}:~/.
    #ssh -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" ${vm_external_ip} "bash `basename ${vm_script_init}`"
    echo -e "\tInstall benchmarking application..."
    echo "TODO"
    #scp -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" "${vm_script_app_install}" ${vm_external_ip}:~/.
    #ssh -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" ${vm_external_ip} "bash `basename ${vm_script_app_install}`"
    file_ebi_benchmark="${folder_tmp}"/"${vm_name}-ebi.sh"
    file_cloud_benchmark="${folder_tmp}"/"${vm_name}-cloud.sh"
    echo -e "\tConfiguring benchmark for ebi '${file_ebi_benchmark}'"
    cp "${vm_script_run_benchmark_template}" "${file_ebi_benchmark}"
    sed -i "s/PLACEHOLDER_RESOLVER_HOST/identifiers.org/g" "${file_ebi_benchmark}"
    sed -i "s/PLACEHOLDER_RESOLVER_PROTOCOL/https/g" "${file_ebi_benchmark}"
    sed -i "s/PLACEHOLDER_TARGET_RESOLVER_SERVICE_NAME/ebi/g" "${file_ebi_benchmark}"
    sed -i "s/PLACEHOLDER_REQUEST_MODE/noapi/g" "${file_ebi_benchmark}"
    sed -i "s/PLACEHOLDER_CURRENT_REGION_NAME/europe/g" "${file_ebi_benchmark}"
    scp -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" "${file_ebi_benchmark}" ${vm_external_ip}:~/.
    echo -e "\tConfiguring benchmark for cloud deployment, '${file_cloud_benchmark}'"
    cp "${vm_script_run_benchmark_template}" "${file_cloud_benchmark}"
    sed -i "s/PLACEHOLDER_RESOLVER_HOST/resolver.api.identifiers.org/g" "${file_cloud_benchmark}"
    sed -i "s/PLACEHOLDER_RESOLVER_PROTOCOL/http/g" "${file_cloud_benchmark}"
    sed -i "s/PLACEHOLDER_TARGET_RESOLVER_SERVICE_NAME/cloud/g" "${file_cloud_benchmark}"
    sed -i "s/PLACEHOLDER_REQUEST_MODE/api/g" "${file_cloud_benchmark}"
    sed -i "s/PLACEHOLDER_CURRENT_REGION_NAME/${region}/g" "${file_cloud_benchmark}"
    scp -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" "${file_cloud_benchmark}" ${vm_external_ip}:~/.
    echo -e "\tLaunching benchmarks"
    ssh -f -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" ${vm_external_ip} "nohup bash `basename ${file_cloud_benchmark}` > app/reports/`basename ${file_cloud_benchmark}`.log 2>&1 &"
    ssh -f -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" ${vm_external_ip} "nohup bash `basename ${file_ebi_benchmark}` > app/reports/`basename ${file_ebi_benchmark}`.log 2>&1 &"
done

echo "[[[ --- Starting Results collection --- ]]]"
echo "${created_vms_and_ips[@]}"
echo "${created_vms_and_zones[@]}"
echo "${created_vms[@]}"
for vm_name in "${created_vms[@]}"; do
    ip_address=`gcloud compute instances list --filter=${vm_name} --format=yaml | grep natIP | cut -f2 -d':' | awk '{$1=$1;print}'`
    echo "---> Collecting results from ${vm_name} at ${ip_address}"
    n_reports=`ssh -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" ${ip_address} "ls -alh app/reports/*csv" 2> /dev/null | wc -l | awk '{$1=$1;print}'`
    while [ "$n_reports" != "4" ]; do
        echo "This node is not finished yet, wait a few seconds..."
        sleep 7
        n_reports=`ssh -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" ${ip_address} "ls -alh app/reports/*csv" 2> /dev/null | wc -l | awk '{$1=$1;print}'`
    done
    echo -e "\tCollecting reports..."
    scp -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" ${vm_external_ip}:~/app/reports/* "${folder_reports}"/.
    vm_zone=`gcloud compute instances list --filter=resolver-benchmarkvm-europe-west4 --format=yaml | grep zone:`
    vm_zone="${vm_zone##*/}"
    echo -e "\tDecommissioning VM '${vm_name}', zone '${vm_zone}'"
done
