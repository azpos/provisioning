import subprocess

from typing import Annotated

import eliot
import rich
import typer

import pyposeidon.model as pmodel

from .cli.cluster_app import cluster_app
from .cli.data_app import data_app
from .cli.model_app import model_app
from .tools import run


BDAP_BASE_URL = "https://jeodpp.jrc.ec.europa.eu/ftp/private/{bdap_username}/{bdap_password}/output-ftp/ECMWF/Operational/HRES/LATEST/Data/GRIB/"

app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    help=f"Seareport: A global model",
)
app.add_typer(cluster_app, name="cluster")
app.add_typer(data_app, name="data")
app.add_typer(model_app, name="model")


@app.command()
@eliot.log_call
def login(
    # fmt: off
    timeout: Annotated[int, typer.Option(help="The timeout countdown. If it expires, you probably haven't setup the managed identity correctly.")] = 5,
    # fmt: on
) -> int:
    """ Login to azure-cli and azcopy using system-managed-identity """
    cmds = [
        "az login --identity",
        "azcopy login --identity"
    ]
    for cmd in cmds:
        try:
            run(cmd=cmd, check=False, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            rich.print(f"[yellow]{cmd}[/yellow]: [bold red]Fail...")
            rich.print("The command [italic]timed out[/italic]. This probably means that you need haven't setup the managed identity correctly.")
            raise typer.Abort() from exc
        else:
            rich.print(f"[yellow]{cmd}[yellow]: [bold green]Success!")
