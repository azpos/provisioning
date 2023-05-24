#!/usr/bin/env bash

set -Eeuo pipefail

source utils.sh

log "START of: AZURE-CLI"

wget https://aka.ms/InstallAzureCLIDeb -O /tmp/install_azure_cli.sh
chmod +x /tmp/install_azure_cli.sh
sudo /tmp/install_azure_cli.sh -y
rm -rf /tmp/install_azure_cli.sh

az login --identity

log "END of: AZURE-CLI"
