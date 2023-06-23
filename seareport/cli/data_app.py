import datetime
import enum
import os
import pathlib
import shutil


from typing import Annotated

import pandas as pd
import rich
import strenum
import typer
import xarray as xr

from seareport import tools
from seareport.cli.tools import BASE_RPATH_OPTION
from seareport.cli.tools import MODEL_NAME_OPTION
from seareport.cli.tools import SHOW_OUTPUT_OPTION
from seareport.cli.tools import SHOW_TRACEBACK_OPTION
from seareport.cli.tools import TIMESTAMP_OPTION


data_app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Handle [blue]seareport[/blue]'s data.",
)


class SeareportModel(strenum.StrEnum):
    iceland = enum.auto()
    global_v1 = enum.auto()
    global_v2 = enum.auto()


def _retrieve_ecmwf_credentials_from_env() -> tuple[str, str]:
    username = os.environ["ECMWF_USERNAME"]
    password = os.environ["ECMWF_PASSWORD"]
    return username, password


def _retrieve_ecmwf_credentials_from_keyvault() -> tuple[str, str]:
    raise NotImplementedError


def retrieve_ecmwf_credentials() -> tuple[str, str]:
    for func in (_retrieve_ecmwf_credentials_from_keyvault, _retrieve_ecmwf_credentials_from_env):
        try:
            username, password = func()
            if username and password:
                return (username, password)
        except (KeyError, NotImplementedError):
            continue
    raise ValueError("Failed to retrieve ECMWF credentials")


def auth_sanity_check(username: str, password: str, mandatory: bool = False) -> None:
    if mandatory or (username or password):
        if not (username and password):
            print("If credentials are provided, both username and password must be present")
            raise typer.Abort()


# def _get_ecmwf_url(timestamp: pd.Timestamp, username: str, password: str) -> str:
#     url = f"ftp://{username}:{password}@aux.ecmwf.int/tcyc/{timestamp.strftime('%Y%m%d.%H')}.tropical_cyclone.grib"
#     return url


@data_app.command()
def from_url(
    # fmt: off
    url: Annotated[str, typer.Option(help="The url for the GRIB file")],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    username: Annotated[str, typer.Option(help="The username (if required).")] = "",
    password: Annotated[str, typer.Option(help="The password (if required).")] = "",
    # fmt: on
) -> int:
    """
    Download GRIB file from the provided [blue]url[/blue] and store it to [blue]base_rpath[/blue].

    """
    auth_sanity_check(username=username, password=password)
    auth = (username, password)
    tools.retrieve_grib(url=url, destination=base_rpath, auth=auth)
    return 0


def ecmwf_url_from_timestamp(timestamp: pd.Timestamp) -> str:
    url = f"ftp://aux.ecmwf.int/tcyc/{timestamp.strftime('%Y%m%d.%H')}.tropical_cyclone.grib"
    return url


@data_app.command()
def from_ecmwf(
    # fmt: off
    timestamp: Annotated[datetime.datetime, TIMESTAMP_OPTION],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    # fmt: on
) -> int:
    """
    Download GRIB file from ECMWF's [blue]FTP[/blue] server and store it to [blue]destination[/blue].

    This requires the following ENV variables:

    - ECMWF_USERNAME
    - ECMWF_PASSWORD

    """
    auth = retrieve_ecmwf_credentials()
    url = ecmwf_url_from_timestamp(timestamp)
    tools.retrieve_grib(url=url, destination=base_rpath, auth=auth)


@data_app.command()
def from_blob(
    # fmt: off
    timestamp: Annotated[datetime.datetime, TIMESTAMP_OPTION],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    container: Annotated[str, typer.Option(help="The url of the container that contains the grib file.")] = "https://ppwdevarchivecoolsa.blob.core.windows.net/ecmwf",
    show_output: Annotated[bool, SHOW_OUTPUT_OPTION] = True,
    show_traceback: Annotated[bool, SHOW_TRACEBACK_OPTION] = False,
    # fmt: on
) -> int:
    """
    Download GRIB file from Blob and store it to [blue]destination[/blue].
    """
    url = tools.get_blob_url_from_timestamp(container=container, ts=timestamp)
    cmd = f"azcopy copy {url} {str(base_rpath)}"
    tools.run_cli(cmd, show_traceback=show_traceback, show_output=show_output)


@data_app.command()
def get_base_model(
    # fmt: off
    model_name: Annotated[SeareportModel, MODEL_NAME_OPTION],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    show_output: Annotated[bool, SHOW_OUTPUT_OPTION] = True,
    show_traceback: Annotated[bool, SHOW_TRACEBACK_OPTION] = False,
    # fmt: on
) -> int:
    """
    Download and extract the specified model at [blue]path[/blue].
    """
    archive_name = f"{model_name}.tar.zst"
    url = f"https://ppwdevarchivesa.blob.core.windows.net/base-models/{archive_name}"
    dst = base_rpath / archive_name

    with tools.cli_log(f"Downloading base model: {model_name}"):
        cmd = f"azcopy copy {url} {dst}"
        tools.run_cli(cmd=cmd, show_output=show_output, show_traceback=show_traceback)

    with tools.cli_log(f"Extracting base model: {archive_name}"):
        cmd = f"tar -C {base_rpath} -xvf {dst}"
        tools.run_cli(cmd=cmd,  show_output=show_output, show_traceback=show_traceback)


@data_app.command()
def get_pack(
    # fmt: off
    model_name: Annotated[SeareportModel, MODEL_NAME_OPTION],
    timestamp: Annotated[datetime.datetime, TIMESTAMP_OPTION],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    # fmt: on
) -> int:
    """
    Download and extract the specified model's pack
    """
    archive_name = f"{timestamp.strftime('%Y%m%d.%H')}.tar.zst"
    url = f"https://ppwdevarchivecoolsa.blob.core.windows.net/{model_name}-packs/{archive_name}"
    dst = base_rpath / archive_name

    with tools.cli_log(f"Downloading pack for {model_name}: {archive_name}"):
        cmd = f"azcopy copy {url} {dst}"
        tools.run_cli(cmd=cmd, show_output=False, show_traceback=True)


@data_app.command()
def upload_results(
    # fmt: off
    model_name: Annotated[SeareportModel, MODEL_NAME_OPTION],
    timestamp: Annotated[datetime.datetime, TIMESTAMP_OPTION],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    # fmt: on
) -> int:
    """
    Upload model results to Blob
    """
    model_rpath = tools.get_rpath_from_timestamp(base_rpath=base_rpath, timestamp=timestamp)

    netcdf = model_rpath.parent / f"{model_rpath.name}.nc"
    staout = model_rpath.parent / f"{model_rpath.name}.staout_1.zip"
    pack = model_rpath.parent / f"{model_rpath.name}.tar.zst"

    if not netcdf.exists():
        rich.print(f"\n[bold red]Missing output file: {netcdf}")
        rich.print("[bold red]Post-process the data and try again!")
        raise typer.Abort()
    with tools.cli_log(f"Uploading: {netcdf}"):
        url = f"https://ppwdevarchivesa.blob.core.windows.net/{model_name}-results/"
        cmd = f"azcopy copy {netcdf} {url}"
        tools.run_cli(cmd=cmd, show_output=True, show_traceback=True)
    with tools.cli_log(f"Uploading: {staout}"):
        url = f"https://ppwdevarchivesa.blob.core.windows.net/{model_name}-results/"
        cmd = f"azcopy copy {staout} {url}"
        tools.run_cli(cmd=cmd, show_output=True, show_traceback=True)
    if not pack.exists():
        rich.print(f"\n[bold red]Missing pack file: {pack}")
        rich.print("[bold red]Post-process the data and try again!")
        raise typer.Abort()
    with tools.cli_log(f"Uploading: {pack}"):
        url = f"https://ppwdevarchivecoolsa.blob.core.windows.net/{model_name}-packs/"
        cmd = f"azcopy copy {pack} {url}"
        tools.run_cli(cmd=cmd, show_output=True, show_traceback=True)

    with tools.cli_log(f"Cleaning up!", "Cleaning up: Successful!"):
        netcdf.unlink()
        pack.unlink()
        shutil.rmtree(model_rpath)
