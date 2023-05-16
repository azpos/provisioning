#!/usr/bin/env bash
#

source 010_globals.sh

export GROUP_NAME="${CONTROL}"
export GROUP_PREFIX="${CONTROL_PREFIX}"
export RESOURCE_GROUP="${GROUP_PREFIX}"-rg

export CONTROL_VM_NAME="${GROUP_PREFIX}"-vm
