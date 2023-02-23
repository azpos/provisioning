#!/usr/bin/env bash
#

set -Eeuo pipefail

log() {
  printf '%s - %05d sec - %s\n' "$(date +'%T.%3N')" ${SECONDS} "${*}"
  SECONDS=0
}

debug() {
  printf '    %s\n' "${*}"
}
