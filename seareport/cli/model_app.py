import enum
import datetime
import inspect
import os
import pathlib
import sys

from typing import Annotated

import typer

model_app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    help=f"Handle seareport's model",
)


@model_app.command()
def init() -> int:
    """ Create the cluster. """


@model_app.command()
def generate() -> int:
    """ Generate the model for the provided run. """


@model_app.command()
def run() -> int:
    """ Execute the model. """


@model_app.command()
def post() -> int:
    """ Post-process the model. """

