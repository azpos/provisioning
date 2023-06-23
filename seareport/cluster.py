from __future__ import annotations

import shutil

import eliot
import rich
import typer

from .azcli import check_azcli_logged_in
from .settings import check_settings
from .settings import Settings
from .tools import run_cli


SCALE_CMD = """
az vmss scale \\
  --resource-group {settings.project}-{settings.environment}-compute-rg \\
  --name {settings.project}-{settings.environment}-compute-vmss \\
  --new-capacity {capacity} \\
  --output json
""".strip()


@eliot.log_call
def cluster_sanity_check() -> None:
    check_settings()
    check_executables_are_available()
    check_azcli_logged_in()


def check_executables_are_available():
    for exec in ["az", "azcopy", "ansible-playbook"]:
        if not shutil.which(exec):
            rich.print(
                f"Executable [bold green]{exec}[/bold green] cannot be found in [bold]$PATH[/bold]. Please install it and try again."
            )
            raise typer.Abort()


@eliot.log_call
def cluster_scale(capacity: int, show_traceback: bool, show_output: bool) -> None:
    cluster_sanity_check()
    settings = Settings()
    cmd = SCALE_CMD.format(settings=settings, capacity=capacity)
    run_cli(cmd=cmd, show_traceback=show_traceback, show_output=show_output)
