#!/usr/bin/env bash
#

set -Eeuo pipefail

source utils.sh
source ~/.bashrc

log "START of: PIPX setup"

echo $PATH

if [ ! -x "$(command -v pipx)" ]; then
  python3.10 -m pip install --no-warn-script-location --user pipx
fi

log "END of: PIPX setup"
