#ª/bin/bash
# Install the benchmarking application as regular user
# Author: Manuel Bernal Llinares <mbdebian@gmail.com>

git clone https://github.com/identifiers-org/cloud-devops-benchmarking.git app
cd app
alias pip='pip3'
make install
