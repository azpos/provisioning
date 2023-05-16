#!/usr/bin/env bash
#

set -Eeuo pipefail

source 300_control_variables.sh

set -x

: " ----> Creating group: ${RESOURCE_GROUP}"
az group create \
  --location "${LOCATION}" \
  --tags project="${PROJECT}" \
          environment="${ENVIRONMENT}" \
          location="${LOCATION}" \
          group="${GROUP_NAME}" \
  --name "${RESOURCE_GROUP}"
: " ----> Created group: ${RESOURCE_GROUP}"
