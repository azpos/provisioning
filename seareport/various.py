from __future__ import annotations

import subprocess

import rich
import typer

from .settings import Settings
from .tools import run

import tenacity


def retry_attempts(no_attempts: int, exception_type: Exception) -> tenacity.Retrying:
    retrying = tenacity.Retrying(
        stop=tenacity.stop_after_attempt(no_attempts),
        retry=tenacity.retry_if_exception_type(exception_type),
        wait=tenacity.wait_fixed(1) + tenacity.wait_random(1, 3),
    )
    return retrying


def do_login(cmd: str, timeout: int, no_attempts: int = 3) -> None:
    try:
        for i, attempt in enumerate(retry_attempts(no_attempts, subprocess.TimeoutExpired), 1):
            with attempt:
                try:
                    run(cmd=cmd, check=False, timeout=timeout)
                except subprocess.TimeoutExpired:
                    rich.print(f"[italic]{cmd}[/italic] [red]failed[/red]. [bold]{i}/{no_attempts}[/bold] attempts...")
                    raise
                else:
                    rich.print(f"[yellow]{cmd}[yellow]: [bold green]Success!")
    except tenacity.RetryError as exc:
        rich.print(f"[yellow]{cmd}[/yellow]: [bold red]Fail...")
        rich.print(
            f"The command [italic]timed out[/italic] {no_attempts} times in a row. This probably means that you need haven't setup the managed identity correctly."
        )
        raise typer.Abort() from exc


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
