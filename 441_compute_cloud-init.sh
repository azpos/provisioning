#!/usr/bin/env bash

set -xeuo pipefail

runuser --pty -u azuser -- ansible-pull -U https://github.com/azpos/provisioning playbooks/compute/playbook.yml -i "$(hostname --short),"
