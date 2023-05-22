#!/usr/bin/env bash

set -Eeuo pipefail

source utils.sh

mdadm --create --verbose /dev/md0  --level=0 --metadata=1.2 --name=NVME_RAID --raid-devices=2 /dev/nvme0n1 /dev/nvme1n1
mkfs.ext4 -L RAID0 /dev/md0
mkdir -p /scratch
mount LABEL=RAID0 /scratch
chown $(id azuser -u):$(id azuser -g) /scratch
