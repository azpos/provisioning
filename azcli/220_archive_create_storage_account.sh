#!/usr/bin/env bash
#

set -Eeuo pipefail

source ./200_archive_variables.sh

set -x

: " ----> Creating storage_account: ${RESOURCE_GROUP}"
# Add a storage account reference to the Batch account for use as 'auto-storage'
# for applications. Start by creating the storage account.
az storage account create \
    --name "${STORAGE_ACCOUNT}" \
    --location "${LOCATION}" \
    --resource-group "${RESOURCE_GROUP}" \
    --sku Standard_LRS \
    --access-tier 'Hot' \
    --kind 'StorageV2' \
    --allow-blob-public-access true \
    --allow-shared-key-access true \
    --default-action allow \
    --enable-hierarchical-namespace \
    --enable-local-user false \
    --enable-nfs-v3 \
    --encryption-services 'blob' \
    --https-only true \
    --min-tls-version TLS1_2 \
    --public-network-access Enabled \
    --subnet /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_PREFIX}"-rg/providers/Microsoft.Network/virtualNetworks/"${VNET}"/subnets/"${COMPUTE_SNET}" \
    --tags project="${PROJECT}" \
           environment="${ENVIRONMENT}" \
           location="${LOCATION}" \
           group="${GROUP_NAME}" \
    --output yamlc

# Find storage key
storage_key="$( az storage account keys list --account-name "${STORAGE_ACCOUNT}" --resource-group ${RESOURCE_GROUP} --query [0].value  --output tsv )"
echo "${storage_key}"

myip=$(curl -s http://whatismyip.akamai.com/)

# whitelist our IP
az storage account network-rule add --ip-address "${myip}" --account-name "${STORAGE_ACCOUNT}" --output yamlc

# Create storage container
az storage container create \
  --name "${SEAREPORT_CONTAINER}" \
  --account-name "${STORAGE_ACCOUNT}" \
  --account-key "${storage_key}" \
  --output yamlc

az storage account network-rule remove --ip-address "${myip}" --account-name "${STORAGE_ACCOUNT}" --output yamlc
