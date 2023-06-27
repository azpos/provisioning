from typing import Annotated

import eliot
import typer

from .cluster_app import cluster_app
from .data_app import data_app
from .model_app import model_app
from ..various import do_login
from ..various import healthcheck as api_healthcheck


BDAP_BASE_URL = "https://jeodpp.jrc.ec.europa.eu/ftp/private/{bdap_username}/{bdap_password}/output-ftp/ECMWF/Operational/HRES/LATEST/Data/GRIB/"

app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    rich_markup_mode="rich",
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
    no_attempts: Annotated[int, typer.Option(help="How many times to retry to login")] = 3,
    # fmt: on
) -> int:
    """Login to [blue]azure-cli[/blue] and [blue]azcopy[/blue] using [italic]system-managed-identity[/italic]."""
    do_login("az login --identity", timeout=timeout, no_attempts=no_attempts)
    do_login("azcopy login --identity", timeout=timeout, no_attempts=no_attempts)


@app.command()
@eliot.log_call
def healthcheck() -> int:
    """
    Check that all the necessary resources have been created
    """
    api_healthcheck()
