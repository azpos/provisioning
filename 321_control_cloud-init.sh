#!/usr/bin/env bash

set -xeuo pipefail

export ANSIBLE_CALLBACKS_ENABLED=ansible.posix.profile_tasks
runuser --pty -u azuser -w ANSIBLE_CALLBACKS_ENABLED -- ansible-pull -U https://github.com/azpos/provisioning playbooks/control/playbook.yml -i "$(hostname --short),"
