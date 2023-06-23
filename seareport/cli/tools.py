from __future__ import annotations

import typer


def get_existing_dir_option(help: str = ""):
    return typer.Option(
        dir_okay=True,
        exists=True,
        file_okay=False,
        help=help,
        readable=True,
        resolve_path=True,
        writable=True,
    )


def get_existing_file_option(help: str = ""):
    return typer.Option(
        dir_okay=False,
        exists=True,
        file_okay=True,
        help=help,
        readable=True,
        resolve_path=True,
        writable=True,
    )


BASE_RPATH_OPTION = get_existing_dir_option("The directory inside which to save the data.")
BASE_MODEL_OPTION = get_existing_dir_option(help="The directory containing the base model")
MODEL_NAME_OPTION = typer.Option(help="The name of the model.")

SHOW_TRACEBACK_OPTION = typer.Option(help="In case of errors, show the full python traceback")
SHOW_OUTPUT_OPTION = typer.Option(help="Show the output of the command")
TIMESTAMP_OPTION = typer.Option(help="The timestamp for which we want to operate.")
