#!/usr/bin/env bash
#

set -Eeuo pipefail

source 400_compute_variables.sh

set -x

: " ----> Creating Proximity Placement Group: ${PPG_NAME}"
az ppg create \
  --resource-group "${RESOURCE_GROUP}" \
  --name "${PPG_NAME}" \
  --location "${LOCATION}" \
  --intent-vm-sizes \
      Standard_HB120rs_v3 \
      Standard_HB120-96rs_v3 \
      Standard_HB120-64rs_v3 \
      Standard_HB120-32rs_v3 \
      Standard_HB120rs_v2 \
      Standard_HB120-96rs_v2 \
      Standard_HB120-64rs_v2 \
      Standard_HB120-32rs_v2 \
  --tags project="${PROJECT}" \
          environment="${ENVIRONMENT}" \
          location="${LOCATION}" \
          group="${GROUP_NAME}" \
  --zone 2 \
| jq
: " ----> Created Proximity Placement Group: ${PPG_NAME}"
