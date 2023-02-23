#!/usr/bin/env bash
#

set -euo pipefail

source utils.sh

metadata_json='/tmp/metadata.json'

log Starting: metadata parsing
cmd="timeout 3 curl --fail --silent -H Metadata:true --noproxy '*' 'http://169.254.169.254/metadata/instance?api-version=2021-02-01' > ${metadata_json}"
debug "${cmd}"
eval "${cmd}"

PROJECT=$(jq  '.compute.tagsList[] | select(.name == "project") | .value' "${metadata_json}")
ENVIRONMENT=$(jq  '.compute.tagsList[] | select(.name == "environment") | .value' "${metadata_json}")

export PROJECT
export ENVIRONMENT

log Finished: metadata parsing
