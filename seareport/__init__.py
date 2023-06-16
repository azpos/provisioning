import enum
import datetime
import inspect
import os
import pathlib
import sys

from typing import Annotated

import typer

import pyposeidon.model as pmodel

from .cli.cluster_app import cluster_app
from .cli.data_app import data_app
from .cli.model_app import model_app

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


# _MANDATORY_ENV_VARIABLES = {
#     "download": (
#         "GRIB_USERNAME",
#     ),
# }
#
# def sanity_check() -> None:
#     caller_function_name  = inspect.stack()[1][3]
#     missing = []
#     for name in _MANDATORY_ENV_VARIABLES[caller_function_name]:
#         env_name = f"SEAREPORT_{name}"
#         env_value = os.environ.get(env_name)
#         if not env_value:
#             missing.append(env_name)
#     if missing:
#         msg = f"The following ENV variables are required. Please define them and run again:\n{missing}"
#         sys.exit(msg)



# @app.command(no_args_is_help=True)
# def main(
#     # fmt: off
#     base_model: Annotated[pathlib.Path, typer.Argument(help="The path to the base model. If it is a URL the model will be downloaded.")],
#     meteo: Annotated[pathlib.Path, typer.Argument(help="The path to the input Meteo file. If it is a URL it will be downloaded")],
#     # fmt: on
# ) -> int:
#     print(str(base_model))
#     print(str(meteo))
#     return 0

