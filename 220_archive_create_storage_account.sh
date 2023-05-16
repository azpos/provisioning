#!/usr/bin/env bash
#

set -Eeuo pipefail

source 200_archive_variables.sh

set -x

SA="ppw-dev-archive-hot-sa"
SEAREPORT="seareport"

: " ----> Creating storage_account: ${RESOURCE_GROUP}"
# Add a storage account reference to the Batch account for use as 'auto-storage'
# for applications. Start by creating the storage account.
az storage account create \
    --name "${SA}" \
    --location "${LOCATION}" \
    --resource-group "${RESOURCE_GROUP}" \
    --sku Standard_LRS \
    --access-tier 'Hot' \
    --kind 'StorageV2' \
    --enable-hierarchical-namespace \
    --enable-nfs-v3 \
    --encryption-services 'blob' \
    --tags project="${PROJECT}" \
           environment="${ENVIRONMENT}" \
           location="${LOCATION}" \
           group="${GROUP_NAME}" \

# Find storage key
storage_key="$( az storage account keys list --account-name "${SA}" --resource-group ${RESOURCE_GROUP}--query [0].value  --output tsv )"
echo "${storage_key}"

# Create storage container
az storage container create \
  --name "${SEAREPORT}" \
  --account-name "${SA}" \
  --account-key "${storage_key}"
