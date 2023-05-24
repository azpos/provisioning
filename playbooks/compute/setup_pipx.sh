#!/usr/bin/env bash
#

set -Eeuo pipefail

source utils.sh
source ~/.bashrc

log "START of: PIPX setup"

if [ ! -x "$(command -v pipx)" ]; then
  python3.9 -m pip install --no-warn-script-location --user pipx
fi

which pipx

log "END of: PIPX setup"
