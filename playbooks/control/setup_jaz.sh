#!/usr/bin/env bash
#

set -Eeuo pipefail

source utils.sh
source ~/.bashrc

log "START of: PIPX install jaz"

python3 -m pipx install jaz

log "END of: PIPX install jaz"
