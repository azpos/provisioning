import datetime
import os
import pathlib

from typing import Annotated

import eliot
import pandas as pd
import typer
import xarray as xr

from eliot import current_action
from eliot import log_message
from eliot import log_call

from seareport import tools


class MyEncoder(eliot.json.EliotJSONEncoder):
    def default(self, obj):
        if isinstance(obj, (pd.Timestamp, pathlib.Path)):
            return str(obj)
        return eliot.json.EliotJSONEncoder.default(self, obj)


eliot.to_file(open("linkcheck.log", "w"), encoder=MyEncoder)


data_app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    help="Handle seareport's data",
)


ExistingDir = typer.Option(
    exists=True,
    file_okay=False,
    dir_okay=True,
    writable=True,
    help="The directory where to save the downloaded GRIB file."
)


@log_call(include_result=False)
def _retrieve_ecmwf_credentials_from_env() -> tuple[str, str]:
    username = os.environ["ECMWF_USERNAME"]
    password = os.environ["ECMWF_PASSWORD"]
    return username, password


@log_call(include_result=False)
def _retrieve_ecmwf_credentials_from_keyvault() -> tuple[str, str]:
    raise NotImplementedError


@log_call(include_result=False)
def retrieve_ecmwf_credentials() -> tuple[str, str]:
    for func in (_retrieve_ecmwf_credentials_from_keyvault, _retrieve_ecmwf_credentials_from_env):
        try:
            username, password = func()
            if username and password:
                return (username, password)
        except (KeyError, NotImplementedError):
            continue
    raise ValueError("Failed to retrieve ECMWF credentials")


@log_call
def auth_sanity_check(username: str, password: str, mandatory: bool = False) -> None:
    if mandatory or (username or password):
        if not (username and password):
            current_action().log("Missing credentials")
            print("If credentials are provided, both username and password must be present")
            raise typer.Abort()


@log_call(include_args=["timestamp"])
def _get_ecmwf_url(timestamp: pd.Timestamp, username: str, password: str) -> str:
    url = f"ftp://{username}:{password}@aux.ecmwf.int/tcyc/{timestamp.strftime('%Y%m%d.%H')}.tropical_cyclone.grib"
    return url


@data_app.command()
@log_call
def from_url(
    # fmt: off
    url: Annotated[str, typer.Argument(help="The url for the GRIB file")],
    destination: Annotated[pathlib.Path, ExistingDir] = pathlib.Path("./"),
    username: Annotated[str, typer.Option(help="The username (if required).")] = "",
    password: Annotated[str, typer.Option(help="The password (if required).")] = "",
    # fmt: on
) -> int:
    """
    Download GRIB file from the provided `url` and store it to `destination`.

    """
    auth_sanity_check(username=username, password=password)
    auth = (username, password)
    tools.retrieve_grib(url=url, destination=destination, auth=auth)
    return 0


@log_call
def ecmwf_url_from_timestamp(timestamp: pd.Timestamp) -> str:
    url = f"ftp://aux.ecmwf.int/tcyc/{timestamp.strftime('%Y%m%d.%H')}.tropical_cyclone.grib"
    return url


@data_app.command()
@log_call
def from_ecmwf(
    # fmt: off
    timestamp: Annotated[datetime.datetime, typer.Argument(help="The timestamp for which we want to download the GRIB file from ECMWF.")],
    destination: Annotated[pathlib.Path, ExistingDir] = pathlib.Path("./"),
    # fmt: on
) -> int:
    """
    Download GRIB file from ECMWF's FTP server and store it to ``destination``.

    This requires the following ENV variables:

    - ECMWF_USERNAME
    - ECMWF_PASSWORD

    """
    auth = retrieve_ecmwf_credentials()
    url = ecmwf_url_from_timestamp(timestamp)
    tools.retrieve_grib(url=url, destination=destination, auth=auth)


@data_app.command()
def store(
    path: Annotated[pathlib.Path, typer.Argument(help="The path to the GRIB file.")],
) -> int:
    """
    Store downloaded GRIB file to Blob

    """
    return 0
