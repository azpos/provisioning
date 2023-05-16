#!/usr/bin/env bash
#

set -euo pipefail

source 100_infra_variables.sh

set -x

: "Creating: ${VNET}"
az network vnet create \
    --name "${VNET}" \
    --location "${LOCATION}" \
    --resource-group "${RESOURCE_GROUP}" \
    --tags project="${PROJECT}" \
           environment="${ENVIRONMENT}" \
           location="${LOCATION}" \
           group="${GROUP_NAME}" \
    --ddos-protection 0 \
    --address-prefix 10.10.0.0/16 \
| jq
: "Created: ${VNET}"
