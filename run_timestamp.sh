#!/usr/bin/env bash
#

source init_conda
conda activate seareport_env

set -euo pipefail

export SEAREPORT_PROJECT=ppw
export SEAREPORT_ENVIRONMENT=dev

export MODEL_NAME=global-v1

export BASE_RPATH=/mnt/BASE_RPATH

mkdir -p "${BASE_RPATH}"
cd "${BASE_RPATH}"

current_timestamp="${1}"
previous_timestamp="${2}"

set -x

ntfy send "${current_timestamp}: Start"

seareport login --timeout 30

seareport data get-base-model --model-name "${MODEL_NAME}"

seareport data get-pack --model-name "${MODEL_NAME}" --timestamp "${previous_timestamp}"

seareport data from-blob --timestamp "${current_timestamp}"

seareport model next --timestamp "${current_timestamp}"

seareport cluster create

seareport model run --ssh --mpi-timeout 40 --timestamp "${current_timestamp}"

seareport cluster destroy

seareport model post --timestamp "${current_timestamp}"

seareport login --timeout 30

seareport data upload-results --model-name "${MODEL_NAME}" --timestamp "${current_timestamp}"

cd
rm -rf "${BASE_RPATH}"

ntfy send "${current_timestamp}: OK"
