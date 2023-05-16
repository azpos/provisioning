#!/usr/bin/env bash

set -xeuo pipefail

export PYTHONUNBUFFERED=True
runuser --pty -u azuser -l -w PYTHONUNBUFFERED -- ansible-pull -U https://github.com/azpos/provisioning playbooks/control/playbook.yml -i "$(hostname --short),"
