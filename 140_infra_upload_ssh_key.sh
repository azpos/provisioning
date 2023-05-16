#!/usr/bin/env bash
#

set -Eeuo pipefail

source 100_infra_variables.sh

set -x

: "Uploading ${SSH_CONNECT_PUBLIC}"
az sshkey create \
  --location "${LOCATION}" \
  --resource-group "${RESOURCE_GROUP}" \
  --public-key "@${SSH_CONNECT_PUBLIC}" \
  --name "${GROUP_PREFIX}-connect-ssh" \
  --tags project="${PROJECT}" \
         environment="${ENVIRONMENT}" \
         location="${LOCATION}" \
         group="${GROUP_NAME}" \
| jq


: "Uploading ${SSH_CLUSTER_PUBLIC}"
az sshkey create \
  --location "${LOCATION}" \
  --resource-group "${RESOURCE_GROUP}" \
  --public-key "@${SSH_CLUSTER_PUBLIC}" \
  --name "${GROUP_PREFIX}-cluster-ssh" \
  --tags project="${PROJECT}" \
         environment="${ENVIRONMENT}" \
         location="${LOCATION}" \
         group="${GROUP_NAME}" \
| jq
