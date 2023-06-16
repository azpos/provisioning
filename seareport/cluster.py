from __future__ import annotations

from eliot import log_call

from .azcli import check_azcli_logged_in
from .settings import check_settings
from .settings import Settings
from .tools import run_cli


SCALE_CMD = """
az vmss scale \\
  --resource-group {settings.project}-{settings.environment}-compute-rg \\
  --name {settings.project}-{settings.environment}-compute-vmss \\
  --new-capacity {capacity} \\
  --output json
""".strip()


@log_call
def cluster_sanity_check() -> None:
    check_settings()
    check_azcli_logged_in()


@log_call
def cluster_scale(capacity: int, show_traceback: bool, show_output: bool) -> None:
    cluster_sanity_check()
    settings = Settings()
    cmd = SCALE_CMD.format(settings=settings, capacity=capacity)
    run_cli(cmd=cmd, show_traceback=show_traceback, show_output=show_output)

