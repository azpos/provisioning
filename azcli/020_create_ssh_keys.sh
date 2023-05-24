#!/usr/bin/env bash

set -euo pipefail


source ./010_globals.sh

set -x

# - The compute key is the one that the HPC nodes are using in order to connect to one another. This is uploaded to the keyvault
#
# The following code creates the keys if they are missing
if [[ ! -f "${SSH_COMPUTE}" ]]; then
  : "Generating ${SSH_COMPUTE} key pair"
  ssh-keygen \
    -m PEM \
    -t rsa \
    -b 4096 \
    -C "coastal-compute@azure" \
    -f "${SSH_COMPUTE}" \
    -N ""
else
  : "${SSH_COMPUTE} key pair already exists. Skipping"
fi
