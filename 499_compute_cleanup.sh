#!/usr/bin/env bash
#

set -euo pipefail

source 400_compute_variables.sh

set -x

: " ----> Deleting group: ${RESOURCE_GROUP}"
az group delete --yes --name "${RESOURCE_GROUP}"
: " ----> Deleted group: ${RESOURCE_GROUP}"
