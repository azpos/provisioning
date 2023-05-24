#!/usr/bin/env bash
#

set -Eeuo pipefail

source utils.sh

log "START of: SCHISM setup"

eval "$(/mnt/mambaforge/condabin/conda shell.bash hook)"
source /mnt/mambaforge/etc/profile.d/conda.sh
which mamba

log "Setup conda env"
mamba create --yes --quiet --name schism_env "pschism=5.9*=mpi_openmpi*" ucx

log "Test conda env"
conda activate schism_env
which schism

log "END of: SCHISM setup"
