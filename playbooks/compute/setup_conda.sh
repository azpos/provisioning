#!/usr/bin/env bash
#

set -Eeuo pipefail

source utils.sh

log "START of: CONDA_SETUP"

wget https://raw.githubusercontent.com/pmav99/posazure/master/condarc -O ~/.condarc
#wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh -O ~/mambaforge.sh
bash ~/mambaforge.sh -b -p /mnt/mambaforge -u
eval "$(/mnt/mambaforge/condabin/conda shell.bash hook)"
source /mnt/mambaforge/etc/profile.d/conda.sh
which mamba

mamba config --add envs_dirs /mnt/envs

log "Setup conda env"
mamba create --yes --quiet --name schism_env "pschism=5.9*=mpi_openmpi*" ucx
mamba create --yes --quiet --name pyposeidon_env pyposeidon-base=0.6.0

log "Test conda env"
conda activate schism_env
which schism

rm -rf ~/mambaforge.sh
log "END of: CONDA_SETUP"
