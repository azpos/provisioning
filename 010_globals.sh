#!/usr/bin/env bash

set -euo pipefail

source 000_parameters.sh

# export SSH_PRIVATE_KEY=~/.ssh/coastal.pem
# export SSH_PUBLIC_KEY=~/.ssh/coastal.pub.pem

# Group names
export INFRA="infra"
export COMPUTE="compute"
export ARCHIVE="archive"
export CONTROL="control"
# export VISUALZ="visualz"

# Prefixes
export BASE_PREFIX="${PROJECT}"-"${ENVIRONMENT}"
export INFRA_PREFIX="${BASE_PREFIX}"-"${INFRA}"
export ARCHIVE_PREFIX="${BASE_PREFIX}"-"${ARCHIVE}"
export COMPUTE_PREFIX="${BASE_PREFIX}"-"${COMPUTE}"
export CONTROL_PREFIX="${BASE_PREFIX}"-"${CONTROL}"
# export VISUALZ_PREFIX="${BASE_PREFIX}"-"${VISUALZ}"

# Networking - Virtual Network
export VNET="${BASE_PREFIX}"-vnet
export KEYVAULT="${BASE_PREFIX}"-kv

# Networking - Subnets
export COMPUTE_SNET="${COMPUTE_PREFIX}"-snet
export CONTROL_SNET="${CONTROL_PREFIX}"-snet
# export VISUALZ_SNET="${VISUALZ_PREFIX}"-snet

# Networking - Network Security Groups
export COMPUTE_NSG="${COMPUTE_PREFIX}"-nsg
export CONTROL_NSG="${CONTROL_PREFIX}"-nsg
# export VISUALZ_NSG="${VISUALZ_PREFIX}"-nsg

# SECRETS
export COMPUTE_SSH_KEY="${COMPUTE}"-SSH-KEY

export ADMIN_USERNAME=azuser

# We have two different SSH key pairs:
# - The compute key is the one that the HPC nodes are using in order to connect to one another. This is uploaded to the keyvault
export SSH_COMPUTE=~/.ssh/"${BASE_PREFIX}"-compute.pem
export SSH_COMPUTE_PUBLIC="${SSH_COMPUTE}".pub
