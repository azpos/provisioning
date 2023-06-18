from __future__ import annotations

import os
import subprocess

from . import PLAYBOOKS
from . import ROOT_DIR
from .tools import run

import eliot


@eliot.log_call
def create_hosts_file():
    cmd = "jaz playbooks/templates/hosts.yml"
    proc = run(cmd, cwd=ROOT_DIR, check=True)
    (ROOT_DIR / "playbooks/hosts.yml").write_text(proc.stdout)


@eliot.log_call
def exec_playbooks(playbooks: list[str]) -> None:
    for playbook in playbooks:
        cmd = f"ansible-playbook -i hosts.yml {playbook}"
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
def mount_nfs_on_control():
    exec_playbooks(playbooks=["mount_nfs.yml"])


@eliot.log_call
def setup_control():
    exec_playbooks(playbooks=["common.yml", "control.yml"])


@eliot.log_call
def setup_master():
    exec_playbooks(playbooks=["common.yml", "cluster_common.yml", "cluster_master.yml"])


@eliot.log_call
def setup_worker():
    pass


@eliot.log_call
def provision_master(show_traceback: bool, show_output: bool):
    create_hosts_file()
    setup_master()
    mount_nfs_on_control()
