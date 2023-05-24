#!/usr/bin/env bash

set -euo pipefail

AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
AZURE_PRINCIPAL_NAME=$(az ad signed-in-user show --query userPrincipalName -o tsv)

export AZURE_SUBSCRIPTION_ID
export AZURE_PRINCIPAL_NAME

export LOCATION=westeurope
export PROJECT=ppw
export ENVIRONMENT=dev
