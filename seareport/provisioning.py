from __future__ import annotations

import os

from . import PLAYBOOKS
from . import tools

import eliot


@eliot.log_call
def exec_playbook(playbook: str, group: str, **kwargs) -> None:
    if kwargs:
        extra_vars=" ".join(f"{key}={value}" for key, value in kwargs.items())
    else:
        extra_vars = ""
    cmd = f"""ansible-playbook -i hosts.yml -l {group} --extra-vars "{extra_vars}" {playbook}"""
    env = os.environ.copy()
    env["ANSIBLE_CALLBACKS_ENABLED"] = "ansible.posix.profile_tasks"
    env["PYTHONUNBUFFERED"] = "1"
    tools.run_cli(cmd, show_output=True, show_traceback=True, cwd=PLAYBOOKS, env=env)


@eliot.log_call
def exec_playbooks(playbooks: list[str], group: str, **kwargs) -> None:
    tools.create_hosts_file()
    for playbook in playbooks:
        exec_playbook(playbook=playbook, group=group, **kwargs)


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
def launch_schism(timeout: int):
    exec_playbooks(playbooks=["launch_schism.yml"], group="master", timeout=timeout)


@eliot.log_call
def setup_worker():
    pass
