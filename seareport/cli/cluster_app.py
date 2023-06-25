from typing import Annotated
from typing import NoReturn

import eliot
import rich
import typer

from .. import PLAYBOOKS
from ..cluster import cluster_scale
from .. import provisioning
from .tools import SHOW_OUTPUT_OPTION
from .tools import SHOW_TRACEBACK_OPTION


cluster_app = typer.Typer(
    add_completion=False,
    add_help_option=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Create/destroy/scale the cluster.",
)


@cluster_app.command()
@eliot.log_call
def create(
    show_traceback: Annotated[bool, SHOW_TRACEBACK_OPTION] = False,
    show_output: Annotated[bool, SHOW_OUTPUT_OPTION] = False,
) -> int:
    """
    Create the cluster.

    Practically speaking, this means bringing up one HPC node and provisioning it as the master.
    """
    cluster_scale(capacity=1, show_traceback=show_traceback, show_output=show_output)
    provisioning.unmount_nfs_on_control()
    provisioning.setup_master()
    provisioning.mount_nfs_on_control()
    return 0


@cluster_app.command()
@eliot.log_call
def destroy(
    show_traceback: Annotated[bool, SHOW_TRACEBACK_OPTION] = False,
    show_output: Annotated[bool, SHOW_OUTPUT_OPTION] = False,
) -> int:
    """
    Destroy the cluster.
    """
    provisioning.unmount_nfs_on_control()
    cluster_scale(capacity=0, show_traceback=show_traceback, show_output=show_output)
    return 0


@cluster_app.command()
@eliot.log_call
def scale_workers(
    no_workers: Annotated[int, typer.Argument(min=0)],
    show_traceback: Annotated[bool, SHOW_TRACEBACK_OPTION] = False,
    show_output: Annotated[bool, SHOW_OUTPUT_OPTION] = False,
) -> NoReturn:
    """
    Scale the cluster's workers up or down.

    """
    rich.print("[italic bold red]Not implemented")
    raise typer.Exit(2)
