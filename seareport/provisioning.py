from __future__ import annotations

import os

from . import PLAYBOOKS
from . import tools

import eliot


@eliot.log_call
def exec_playbook(playbook: str, group: str) -> None:
    tools.create_hosts_file()
    cmd = f"ansible-playbook -i hosts.yml -l {group} {playbook}"
    env = os.environ.copy()
    env["ANSIBLE_CALLBACKS_ENABLED"] = "ansible.posix.profile_tasks"
    env["PYTHONUNBUFFERED"] = "1"
    tools.run_cli(cmd, show_output=True, show_traceback=True, cwd=PLAYBOOKS, env=env)


@eliot.log_call
def exec_playbooks(playbooks: list[str], group: str) -> None:
    for playbook in playbooks:
        exec_playbook(playbook=playbook, group=group)


@eliot.log_call
def mount_nfs_on_control():
    exec_playbooks(playbooks=["mount_nfs.yml"], group="control")


@eliot.log_call
def unmount_nfs_on_control():
    exec_playbooks(playbooks=["unmount_nfs.yml"], group="control")


@eliot.log_call
def setup_control():
    exec_playbooks(playbooks=["common.yml", "control.yml"], group="control")


@eliot.log_call
def setup_master():
    exec_playbooks(playbooks=["common.yml", "cluster_common.yml", "cluster_master.yml"], group="master")


@eliot.log_call
def setup_worker():
    pass
