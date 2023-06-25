#!/usr/bin/env bash
#

set -euo pipefail

tail -n +1 -f /scratch/shared/rpath/outputs/mirror.out | ts -s '%H:%M:%.S' | ts '%Y-%m-%d %H:%M:%S'
