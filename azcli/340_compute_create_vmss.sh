#!/usr/bin/env bash
#

set -Eeuo pipefail

source ./300_compute_variables.sh

set -x

# overprovision?

# OpenLogic:CentOS-HPC:7_9-gen2
# microsoft-dsvm:ubuntu-hpc:2004
# OpenLogic:CentOS-HPC:7_9-gen2

vm_sku='Standard_HB120rs_v3'

# vmss_name="${GROUP_PREFIX}"-centos-vmss
# image_name='OpenLogic:CentOS-HPC:7_9-gen2:latest'

vmss_name="${GROUP_PREFIX}"-vmss
image_name='microsoft-dsvm:ubuntu-hpc:2004:latest'

if az vmss show --name "${vmss_name}" --resource-group "${RESOURCE_GROUP}" > /dev/null; then
  : "VMSS already exists. Skipping creation: %{vmss_name}"
else
  : "Creating ${vmss_name}"
  az vmss create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${vmss_name}" \
    --computer-name-prefix asdf \
    --enable-agent true \
    --enable-auto-update false \
    --orchestration-mode uniform \
    --eviction-policy delete \
    --priority Spot \
    --max-price -1 \
    --ppg "${PPG_NAME}" \
    --single-placement-group true \
    --image "${image_name}" \
    --custom-data 341_compute_cloud-init.sh \
    --accelerated-networking true \
    --authentication-type all \
    --admin-username azuser \
    --assign-identity '[system]' \
    --tags project="${PROJECT}" \
           environment="${ENVIRONMENT}" \
           location="${LOCATION}" \
           group="${GROUP_NAME}" \
           date="$(date)" \
    --ssh-key-values "${SSH_COMPUTE_PUBLIC}" \
    --vm-sku "${vm_sku}" \
    --zones 2 \
    --lb "" \
    --lb-sku Standard \
    --subnet /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_PREFIX}"-rg/providers/Microsoft.Network/virtualNetworks/"${VNET}"/subnets/"${COMPUTE_SNET}" \
    --nsg /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_PREFIX}"-rg/providers/Microsoft.Network/networkSecurityGroups/"${COMPUTE_NSG}" \
    --instance-count 0 \
    --output yamlc
  : "Created ${vmss_name}"
fi

    # --eviction-policy delete \
    # --priority Regular \
    # --priority Spot \
    # --max-price -1 \

:
: "Adding InfiniBand Driver"
az vmss extension set \
  --vmss-name "${vmss_name}" \
  --resource-group "${RESOURCE_GROUP}" \
  --name InfiniBandDriverLinux \
  --publisher Microsoft.HpcCompute \
  --output yamlc

# It seems that role assignment only works for keyvaults within the same resource group.
# In other words, the `--scope argument seems to be partially parsed  - the first resource-group definition is ignored
# Anyhow, this means that we need to assign a role to the system-managed identity manually
# The caveat is that we need to remove it when teraing donw too.
#     --assign-identity '[system]' \
#     --role '4633458b-17de-408a-b874-0445c86b69e6' \
#     --scope /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_PREFIX}"-rg/providers/Microsoft.KeyVault/vaults/"${KEYVAULT}" \
:
: "Give access to the keyvault to the system-managed identity"
az vmss identity assign \
  --role '4633458b-17de-408a-b874-0445c86b69e6' \
  --scope /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_RG}"/providers/Microsoft.KeyVault/vaults/"${KEYVAULT}" \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${vmss_name}" \
  --output yamlc

az vmss identity assign \
  --role 'Storage Blob Data Contributor' \
  --scope /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${ARCHIVE_RG}"/providers/Microsoft.Storage/storageAccounts/"${STORAGE_ACCOUNT}" \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${vmss_name}" \
  --output yamlc
