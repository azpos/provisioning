#!/usr/bin/env bash
#

set -euo pipefail

source 100_infra_variables.sh

set -x

if az keyvault show --resource-group "${RESOURCE_GROUP}" --name "${KEYVAULT}" > /dev/null ; then
  : "Keyvault ${KEYVAULT} already exists. Skipping creation"
else
  : "Creating ${KEYVAULT}"
  az keyvault create \
    --resource-group "${RESOURCE_GROUP}" \
    --name "${KEYVAULT}" \
    --location "${LOCATION}" \
    --enable-rbac-authorization true \
    --enabled-for-deployment true \
    --enabled-for-disk-encryption true \
    --enabled-for-template-deployment true \
    --tags project="${PROJECT}" \
           environment="${ENVIRONMENT}" \
           location="${LOCATION}" \
           group="${GROUP_NAME}" \
    | jq
  : "Created ${KEYVAULT}"
  sleep 30
fi

: "Assign 'Key Vault Administrator' role to self"
az role assignment create \
  `# Role = Key Vaule Administrator - https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide?tabs=azure-cli#azure-built-in-roles-for-key-vault-data-plane-operations` \
  --role 00482a5a-887f-4fb3-b363-3b7fe8e74483 \
  --assignee "${AZURE_PRINCIPAL_NAME}" \
  --scope /subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourcegroups/"${RESOURCE_GROUP}" \
| jq

:
if az keyvault secret show --vault-name ppw-dev-kv --name ppw-dev-infra-cluster-ssh-key >/dev/null; then
  : "Cluster SSH key already in the keyvault. Skipping"
else
  : "Storing cluster SSH key in the keyvault"
  az keyvault secret set \
    --vault-name "${KEYVAULT}" \
    --name "${GROUP_PREFIX}"-cluster-ssh-key \
    --description "Cluster SSH private key" \
    --file "${SSH_CLUSTER}" \
  | jq 'del(.value)'
fi
