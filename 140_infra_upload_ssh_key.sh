#!/usr/bin/env bash
#

set -Eeuo pipefail

source 100_infra_variables.sh

set -x

: "Uploading ${SSH_COMPUTE_PUBLIC}"
az sshkey create \
  --location "${LOCATION}" \
  --resource-group "${RESOURCE_GROUP}" \
  --public-key "@${SSH_COMPUTE_PUBLIC}" \
  --name "${GROUP_PREFIX}-compute-ssh" \
  --tags project="${PROJECT}" \
         environment="${ENVIRONMENT}" \
         location="${LOCATION}" \
         group="${GROUP_NAME}" \
| jq
