#!/usr/bin/env bash
#

source ./010_globals.sh

export GROUP_NAME="${COMPUTE}"
export GROUP_PREFIX="${COMPUTE_PREFIX}"
export RESOURCE_GROUP="${GROUP_PREFIX}"-rg

export PPG_NAME="${GROUP_PREFIX}"-ppg
