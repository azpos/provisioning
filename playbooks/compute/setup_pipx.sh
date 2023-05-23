#!/usr/bin/env bash
#

set -Eeuo pipefail

source utils.sh
source ~/.bashrc

log "START of: PIPX setup"

python3.9 -m pip install --user pipx
python3.9 -m pipx ensurepath

which pipx

log "END of: PIPX setup"
