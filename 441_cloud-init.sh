#!/bin/bash

set -xEeuo pipefail

runuser --pty -u azuser -- ansible-pull -U https://github.com/azpos/provisioning playbook.yml -i "$(hostname --short),"
