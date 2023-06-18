from __future__ import annotations

import os
import subprocess

from . import PLAYBOOKS
from .tools import create_hosts_file
from .tools import run

import eliot


@eliot.log_call
def exec_playbook(playbook: str, group: str) -> None:
    create_hosts_file()
    cmd = f"ansible-playbook -i hosts.yml -l {group} {playbook}"
    print(cmd)
    env = os.environ.copy()
    env["ANSIBLE_CALLBACKS_ENABLED"]="ansible.posix.profile_tasks"
    env["PYTHONUNBUFFERED"] = "1"
    try:
        proc = run(cmd, cwd=PLAYBOOKS, check=False, env=env)
        proc.check_returncode()
    except subprocess.CalledProcessError:
        print()
        print("STDERR")
        print(proc.stderr)
        raise
    finally:
        print()
        print("STDOUT")
        print(proc.stdout)


@eliot.log_call
def exec_playbooks(playbooks: list[str], group: str) -> None:
    for playbook in playbooks:
        exec_playbook(playbook=playbook, group=group)


@eliot.log_call
def mount_nfs_on_control():
    exec_playbooks(playbooks=["mount_nfs.yml"], group="control")


@eliot.log_call
def setup_control():
    exec_playbooks(playbooks=["common.yml", "control.yml"], group="control")


@eliot.log_call
def setup_master():
    exec_playbooks(playbooks=["common.yml", "cluster_common.yml", "cluster_master.yml"], group="master")


@eliot.log_call
def setup_worker():
    pass


@eliot.log_call
def provision_master(show_traceback: bool, show_output: bool):
    setup_master()
    mount_nfs_on_control()
