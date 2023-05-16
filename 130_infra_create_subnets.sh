#!/usr/bin/env bash
#

set -euo pipefail

source 100_infra_variables.sh

set -x

# Create a network security group
: "Creating ${COMPUTE_NSG}"
az network nsg create \
  --resource-group "${RESOURCE_GROUP}" \
  --location "${LOCATION}" \
  --tags project="${PROJECT}" \
          environment="${ENVIRONMENT}" \
          location="${LOCATION}" \
          group="${GROUP_NAME}" \
  --name "${COMPUTE_NSG}" \
| jq
: "Created ${COMPUTE_NSG}"

# : "${COMPUTE_NSG}": add rule for SSH
# az network nsg rule create \
#   --resource-group "${RESOURCE_GROUP}" \
#   --nsg-name "${COMPUTE_NSG}" \
#   --name Allow-SSH-All \
#   --description 'Allow SSH from the internet' \
#   --access Allow \
#   --protocol Tcp \
#   --direction Inbound \
#   --priority 200 \
#   --source-address-prefix Internet \
#   --source-port-range "*" \
#   --destination-address-prefix "*" \
#   --destination-port-range 22 \
# | jq
# : "${COMPUTE_NSG}": added rule for SSH
#
#
# Create a subnet with service endpoints
az network vnet subnet create \
  --name "${COMPUTE_SNET}" \
  --resource-group "${RESOURCE_GROUP}" \
  --vnet-name "${VNET}" \
  --address-prefix 10.10.0.0/24 \
  --network-security-group "${COMPUTE_NSG}" \
  --service-endpoints "Microsoft.Storage" "Microsoft.KeyVault" \
| jq
