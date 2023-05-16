#!/usr/bin/env bash

set -euo pipefail


source 010_globals.sh

# We have two different SSH key pairs:
# - The connect key is the one we use in order to connect to the cluster. This is NOT uploaded in Azure
# - The cluster key is the one that the HPC nodes are using in order to connect to one another. This is uploaded to the keyvault
#
# The following code creates the keys if they are missing
if [[ ! -f "${SSH_CONNECT}" ]]; then
  : "Generating ${SSH_CONNECT} key pair"
  ssh-keygen \
    -m PEM \
    -t rsa \
    -b 4096 \
    -C "coastal-connect@azure" \
    -f "${SSH_CONNECT}" \
    -N ""
fi

if [[ ! -f "${SSH_CLUSTER}" ]]; then
  : "Generating ${SSH_CLUSTER} key pair"
  ssh-keygen \
    -m PEM \
    -t rsa \
    -b 4096 \
    -C "coastal-cluster@azure" \
    -f "${SSH_CLUSTER}" \
    -N ""
fi
