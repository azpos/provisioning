#!/usr/bin/env bash
#

set -euo pipefail

source 300_control_variables.sh

set -x

: " Remove Control-VM to Keyvault role"
az vm identity remove \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${CONTROL_VM_NAME}" \
  --output yamlc

: " ----> Deleting group: ${RESOURCE_GROUP}"
az group delete --yes --name "${RESOURCE_GROUP}"
: " ----> Deleted group: ${RESOURCE_GROUP}"
