#!/usr/bin/env bash
#

set -euo pipefail

source ./azcli/010_globals.sh

payload=$(jaz templates/jit_policy.json)
az rest \
  --method PUT \
  --uri "/subscriptions/""${AZURE_SUBSCRIPTION_ID}""/resourceGroups/""${CONTROL_RG}""/providers/Microsoft.Security/locations/""${LOCATION}""/jitNetworkAccessPolicies/default?api-version=2020-01-01" \
  --body "${payload}"


payload=$(jaz templates/jit_access.json)
az rest \
  --method POST \
  --uri "/subscriptions/""${AZURE_SUBSCRIPTION_ID}""/resourceGroups/""${CONTROL_RG}""/providers/Microsoft.Security/locations/""${LOCATION}""/jitNetworkAccessPolicies/default/initiate?api-version=2015-06-01-preview" \
  --body "${payload}"
