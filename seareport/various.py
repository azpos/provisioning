from __future__ import annotations

import subprocess

import rich
import typer

from .settings import Settings
from .tools import run


def login(timeout: int) -> None:
    cmds = ["az login --identity", "azcopy login --identity"]
    for cmd in cmds:
        try:
            run(cmd=cmd, check=False, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            rich.print(f"[yellow]{cmd}[/yellow]: [bold red]Fail...")
            rich.print(
                "The command [italic]timed out[/italic]. This probably means that you need haven't setup the managed identity correctly."
            )
            raise typer.Abort() from exc
        else:
            rich.print(f"[yellow]{cmd}[yellow]: [bold green]Success!")


def check_resource_groups():
    settings = Settings()
    cmd = f"az group list -o tsv --tag 'project={settings.project}' --tag 'environment={settings.environment}'"
    proc = run(cmd, check=True)
    for domain in ["infra", "archive", "compute", "control"]:
        rg_name = f"{settings.project}-{settings.environment}-{domain}-rg"
        if rg_name not in proc.stdout:
            rich.print(f"[red]Missing resource group[/red]: [bold]{rg_name}")
            raise typer.Abort()
    rich.print("[bold]Resource groups: [green]OK!")


def healthcheck() -> None:
    check_resource_groups()
