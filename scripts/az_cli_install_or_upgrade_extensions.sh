#!/usr/bin/env bash
#

set -euo pipefail

for name in 'account' 'quota' 'ssh' 'storage-preview'; do
  echo Installing/upgrading az extension: "${name}"
  timeout 20 \
    az extension add \
      --name "${name}" \
      --upgrade \
      --output yamlc
done
