import pathlib

import datetime
from typing import Annotated

import click
import rich
import typer
import typer.rich_utils

from seareport import models
from seareport import tools
from seareport.cli.tools import get_existing_dir_option
from seareport.cli.tools import get_existing_file_option

from .tools import BASE_RPATH_OPTION
from .tools import BASE_MODEL_OPTION
from .tools import SHOW_OUTPUT_OPTION
from .tools import SHOW_TRACEBACK_OPTION
from .tools import TIMESTAMP_OPTION

model_app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help=f"Handle [blue]seareport[/blue]'s model",
)


@model_app.command()
def init(
    # fmt: off
    timestamp: Annotated[datetime.datetime, TIMESTAMP_OPTION],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    base_model: Annotated[pathlib.Path, BASE_MODEL_OPTION] = pathlib.Path("./base_model"),
    # fmt: on
) -> int:
    """
    Generate an initial model.

    The reference date of the model is inferred from the meteo file.
    """
    meteo_file = base_rpath / tools.get_grib_filename_from_timestamp(ts=timestamp)
    models.gen_initial(base_model=base_model, base_rpath=base_rpath, meteo_file=meteo_file)


@model_app.command()
def run(
    # fmt: off
    timestamp: Annotated[datetime.datetime, TIMESTAMP_OPTION],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    ssh: Annotated[bool, typer.Option(help="Flag indicating whether we should try to run schism over SSH or not")] = False,
    # fmt: on
) -> int:
    """Execute the model."""
    model_rpath = tools.get_rpath_from_timestamp(base_rpath=base_rpath, timestamp=timestamp)
    if ssh:
        models.run_model_ssh(model_rpath)
    else:
        models.run_model(model_rpath)


@model_app.command()
def post(
    # fmt: off
    timestamp: Annotated[datetime.datetime, TIMESTAMP_OPTION],
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    # fmt: on
) -> int:
    """Post-process the model."""
    model_rpath = tools.get_rpath_from_timestamp(base_rpath=base_rpath, timestamp=timestamp)
    models.post_process(model_rpath=model_rpath)


@model_app.command()
def next(
    # fmt: off
    timestamp: Annotated[datetime.datetime, TIMESTAMP_OPTION],
    base_model: Annotated[pathlib.Path, BASE_MODEL_OPTION] = pathlib.Path("./base_model"),
    base_rpath: Annotated[pathlib.Path, BASE_RPATH_OPTION] = pathlib.Path("./"),
    # fmt: on
) -> int:
    """Generate the model for the provided meteo-file."""
    meteo_file = base_rpath / tools.get_grib_filename_from_timestamp(ts=timestamp)
    models.gen_next(base_model=base_model, base_rpath=base_rpath, meteo_file=meteo_file)
