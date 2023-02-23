#!/usr/bin/env bash
#

set -Eeuo pipefail

log() {
  printf '%s - %05d sec - %s\n' "$(date +'%T.%3N')" ${SECONDS} "${1}"
  SECONDS=0
}

log "START of: CONDA_SETUP"

wget https://raw.githubusercontent.com/pmav99/posazure/master/condarc -O ~/.condarc
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p ~/miniconda
eval "$(~/miniconda/condabin/conda shell.bash hook)"
source ~/miniconda/etc/profile.d/conda.sh
which conda

log "Setup conda env"
conda create --yes --quiet --name schism_env "pschism=5.9*=mpi_openmpi*" ucx

log "Test conda env"
conda activate schism_env
which schism

log "END of: CONDA_SETUP"
