from __future__ import annotations

import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent
PLAYBOOKS = ROOT_DIR / "playbooks"

# from typing import Annotated
#
# import typer
#
# from .cli.cluster_app import cluster_app
# from .cli.data_app import data_app
# from .cli.model_app import model_app
# from .tools import run
# from .various import login
# from .various import healthcheck


# BDAP_BASE_URL = "https://jeodpp.jrc.ec.europa.eu/ftp/private/{bdap_username}/{bdap_password}/output-ftp/ECMWF/Operational/HRES/LATEST/Data/GRIB/"