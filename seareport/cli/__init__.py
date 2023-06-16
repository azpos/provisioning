from typing import Annotated

import eliot
import typer

from .cluster_app import cluster_app
from .data_app import data_app
from .model_app import model_app
from ..various import login
from ..various import healthcheck as api_healthcheck


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
    login(timeout=timeout)
