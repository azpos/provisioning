#!/usr/bin/env bash
#

set -Eeuo pipefail

source ./400_control_variables.sh

set -x

# overprovision?

# OpenLogic:CentOS-HPC:7_9-gen2
# microsoft-dsvm:ubuntu-hpc:2004
# OpenLogic:CentOS-HPC:7_9-gen2


image_name='microsoft-dsvm:ubuntu-hpc:2004:latest'

if az vm show --name "${CONTROL_VM_NAME}" --resource-group "${RESOURCE_GROUP}" --output yamlc >/dev/null; then
  : "Management VM already exists. Skipping creation: %{CONTROL_VM_NAME}"
else
  : "Creating ${CONTROL_VM_NAME}"
  az vm create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${CONTROL_VM_NAME}" \
    --size "Standard_E4ads_v5" \
    --image "${image_name}" \
    --accelerated-networking true \
    --public-ip-sku Standard \
    --custom-data 421_control_cloud-init.sh \
    --priority Regular \
    --admin-username azuser \
    --assign-identity '[system]' \
    --priority Spot \
    --max-price -1 \
    --eviction-policy 'delete' \
    --ssh-key-values "${SSH_PUBLIC_KEY}" \
    --subnet /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_RG}"/providers/Microsoft.Network/virtualNetworks/"${VNET}"/subnets/"${COMPUTE_SNET}" \
    --nsg /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_RG}"/providers/Microsoft.Network/networkSecurityGroups/"${COMPUTE_NSG}" \
    --tags project="${PROJECT}" \
           environment="${ENVIRONMENT}" \
           location="${LOCATION}" \
           group="${GROUP_NAME}" \
           date="$(date)" \
    --output yamlc
  : "Created ${CONTROL_VM_NAME}"
fi

az vm extension set \
    --resource-group "${RESOURCE_GROUP}" \
    --vm-name "${CONTROL_VM_NAME}" \
    --publisher Microsoft.Azure.ActiveDirectory \
    --name AADSSHLoginForLinux \
    --output yamlc


    # --ssh-key-name /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_PREFIX}"-rg/providers/Microsoft.Compute/sshPublicKeys/"${INFRA_PREFIX}"-connect-ssh

# It seems that role assignment only works for keyvaults within the same resource group.
# In other words, the `--scope argument seems to be partially parsed  - the first resource-group definition is ignored
# Anyhow, this means that we need to assign a role to the system-managed identity manually
# The caveat is that we need to remove it when tearing donw too.
#     --assign-identity '[system]' \
#     --role '4633458b-17de-408a-b874-0445c86b69e6' \
#     --scope /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${INFRA_PREFIX}"-rg/providers/Microsoft.KeyVault/vaults/"${KEYVAULT}" \
:
: "Give access to the keyvault to the system-managed identity"
az vm identity assign \
  --identities '[system]' \
  --role '4633458b-17de-408a-b874-0445c86b69e6' `#Keyvault ` \
  --scope "/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/${INFRA_PREFIX}-rg/providers/Microsoft.KeyVault/vaults/${KEYVAULT}" \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${CONTROL_VM_NAME}" \
  --output yamlc


: "Assign Virtual Machine Contributor to the VM in order to let it scale up/down the scale set"
az vm identity assign \
 --identities '[system]' \
 --role '9980e02c-c2be-4d73-94e8-173b1dc7cf3c' `# Virual machine Contributor` \
 --scope "/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/${COMPUTE_PREFIX}"-rg \
 --resource-group "${RESOURCE_GROUP}" \
 --name "${CONTROL_VM_NAME}" \
 --output yamlc
