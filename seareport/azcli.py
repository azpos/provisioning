from __future__ import annotations

import subprocess

import rich
import typer


from .tools import run
from .settings import Settings



def check_azcli_logged_in() -> None:
    cmd = "az account show"
    try:
        run(cmd)
    except subprocess.CalledProcessError as exc:
        rich.print("Before using seareport you must run: [bold green]az login[/bold green]")
        raise typer.Abort() from exc
