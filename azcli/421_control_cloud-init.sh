#!/usr/bin/env bash

set -xeuo pipefail

export ANSIBLE_CALLBACKS_ENABLED=ansible.posix.profile_tasks
export PYTHONUNBUFFERED=1
runuser --pty -u azuser -w PYTHONUNBUFFERED,ANSIBLE_CALLBACKS_ENABLED -- ansible-pull -vvv -U https://github.com/azpos/provisioning -i "$(hostname --short)," playbooks/common.yml playbooks/control.yml

# sudo --preserve-env=ANSIBLE_CALLBACKS_ENABLED,PYTHONUNBUFFERED runuser --pty -u azuser -w PYTHONUNBUFFERED,ANSIBLE_CALLBACKS_ENABLED -- ansible-pull -U https://github.com/azpos/provisioning -i "$(hostname --short)," playbooks/common.yml playbooks/control.yml
