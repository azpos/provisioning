#!/usr/bin/env bash
#

set -euo pipefail
# set -x

access_token=$(az account get-access-token --subscription "${AZURE_SUBSCRIPTION_ID}" --query 'accessToken' --output tsv)
url=https://management.azure.com/subscriptions/"${AZURE_SUBSCRIPTION_ID}"/resourceGroups/"${CONTROL_RG}"/providers/Microsoft.Security/locations/"${LOCATION}"/jitNetworkAccessPolicies/default?api-version=2020-01-01
payload=$(jaz templates/jit_policy.json)

http \
  --verbose \
  --check-status \
  PUT \
  "${url}" \
  "authorization: Bearer ${access_token}" \
  'Content-Type: application/json' <<< "${payload}"

echo

url=https://management.azure.com/subscriptions/"${AZURE_SUBSCRIPTION_ID}"/providers/Microsoft.Security/jitNetworkAccessPolicies?api-version=2020-01-01
http \
  --check-status \
  "${url}" \
  "authorization: Bearer ${access_token}" \
  'Content-Type: application/json'
