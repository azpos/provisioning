from typing import Annotated
from typing import NoReturn

import eliot
import rich
import typer

from ..cluster import cluster_scale
from ..provisioning import provision_master


cluster_app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    help="Create/destroy/scale the cluster.",
)



SHOW_TRACEBACK = typer.Option("--show-traceback", help="In case of errors, show the full python traceback")
SHOW_OUTPUT = typer.Option("--show-output", help="Show the output of the command")



@cluster_app.command()
@eliot.log_call
def create(
    show_traceback: Annotated[bool, SHOW_TRACEBACK] = False,
    show_output: Annotated[bool, SHOW_OUTPUT] = False,
) -> int:
    """
    Create the cluster.

    Practically speaking, this means bringing up one HPC node and provisioning it as the master.
    """
    cluster_scale(capacity=1, show_traceback=show_traceback, show_output=show_output)
    provision_master(show_traceback=show_traceback, show_output=show_output)
    return 0


@cluster_app.command()
@eliot.log_call
def destroy(
    show_traceback: Annotated[bool, SHOW_TRACEBACK] = False,
    show_output: Annotated[bool, SHOW_OUTPUT] = False,
    ) -> int:
    """
    Destroy the cluster.
    """
    cluster_scale(capacity=0, show_traceback=show_traceback, show_output=show_output)
    return 0


@cluster_app.command()
@eliot.log_call
def scale_workers(
    no_workers: Annotated[int, typer.Argument(min=0)],
    show_traceback: Annotated[bool, SHOW_TRACEBACK] = False,
    show_output: Annotated[bool, SHOW_OUTPUT] = False,
) -> NoReturn:
    """
    Scale the cluster's workers up or down.

    """
    rich.print("[italic bold red]Not implemented")
    raise typer.Exit(2)
