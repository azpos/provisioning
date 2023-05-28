#!/usr/bin/env bash

set -xeuo pipefail

export ANSIBLE_CALLBACKS_ENABLED=ansible.posix.profile_tasks
runuser --pty -u azuser -w ANSIBLE_CALLBACKS_ENABLED -- ansible-pull -U https://github.com/azpos/provisioning -i "$(hostname --short)," playbooks/common.yml playbooks/cluster_common.yml
