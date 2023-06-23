from __future__ import annotations

import contextlib
import ftplib
import logging
import pathlib
import shlex
import shutil
import subprocess
import tempfile
import time
import urllib.parse


import httpx
import pandas as pd
import rich.progress
import typer
import xarray as xr

from . import PLAYBOOKS

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def cli_log(pre: str, post: str = ""):
    rich.print(f"\n[italic yellow]{pre}")
    yield
    if post:
        rich.print(f"\n[italic bold green]{post}")


def move(src: pathlib.Path, dst: pathlib.Path) -> None:
    shutil.move(src, dst)


def run(cmd: str, verbose: bool = False, check: bool = True, **kwargs) -> subprocess.CompletedProcess:
    t1 = time.perf_counter()
    proc = subprocess.run(shlex.split(cmd), check=False, capture_output=True, text=True, **kwargs)
    logger.debug(f"Executed {cmd.split(' ')[0]} in {time.perf_counter() - t1:.3f} seconds")
    if check and proc.returncode:
        rich.print("\nSomething went wrong:\n")
        rich.print(f"[bold]{proc.stderr}[bold]")
        proc.check_returncode()
    return proc


def run_cli(
    cmd: str, show_traceback: bool, show_output: bool, msg: str = "Executing:", **kwargs
) -> subprocess.CompletedProcess:
    rich.print(f"\n[italic yellow]{msg}\n")
    rich.print(f"[bold]{cmd}[bold]")
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True, shell=True, **kwargs)
    if proc.returncode:
        rich.print("\n[italic bold red]Something went wrong:\n")
        rich.print(f"[bold]{proc.stderr}[bold]")
        try:
            proc.check_returncode()
        except subprocess.CalledProcessError as exc:
            if show_output:
                print(proc.stdout)
            if show_traceback:
                print(proc.stderr)
                raise
            else:
                raise typer.Abort() from exc
    else:
        rich.print("\n[italic bold green]Finished successfully!")
        if show_output:
            print()
            rich.print(f"[light grey]{proc.stdout}")

    return proc


def get_progress_bar(refresh_per_second: int = 5) -> rich.progress.Progress:
    pbar = rich.progress.Progress(
        "[progress.percentage]{task.percentage:>3.0f}%",
        rich.progress.BarColumn(bar_width=None),
        rich.progress.DownloadColumn(),
        rich.progress.TransferSpeedColumn(),
        refresh_per_second=refresh_per_second,
    )
    return pbar


# Adapted from From https://www.python-httpx.org/advanced/#monitoring-download-progress
def download_httpx(url: str, destination: pathlib.Path, auth: tuple[str, str] | None = None) -> pathlib.Path:
    """
    Download file hosted at `url` and save it to a temporary file in `destination`.

    The function should be used with HTTP urls.
    """
    # Parse url
    parsed_url = urllib.parse.urlparse(url)
    path = pathlib.Path(parsed_url.path)
    filename = path.name

    with httpx.Client(auth=auth) as client:
        with client.stream("GET", url) as response:
            response.raise_for_status()
            total_size = int(response.headers["Content-Length"])
            with tempfile.NamedTemporaryFile(delete=False, dir=destination) as fd:
                dst_path = destination / fd.name
                with get_progress_bar() as pbar:
                    download_task = pbar.add_task("Download", total=total_size)
                    pbar.console.print(f"Downloading {url} to {dst_path}")
                    for chunk in response.iter_bytes():
                        fd.write(chunk)
                        pbar.update(download_task, completed=response.num_bytes_downloaded)
                return destination / fd.name


def download_ftplib(
    url: str,
    destination: pathlib.Path,
    auth: tuple[str, str] | None = None,
    block_size: int = 1024 * 8,
) -> str:
    # Parse url
    parsed_url = urllib.parse.urlparse(url)
    path = pathlib.Path(parsed_url.path)
    parent = path.parent
    filename = path.name

    ftp = ftplib.FTP(parsed_url.netloc)
    if auth:
        ftp.login(*auth)
    ftp.cwd(str(parent))
    ftp.voidcmd("TYPE I")
    socket, size = ftp.ntransfercmd(f"RETR {filename}")

    with tempfile.NamedTemporaryFile(delete=False, dir=destination) as fd:
        dst_path = destination / fd.name
        with get_progress_bar() as pbar:
            download_task = pbar.add_task("Download", total=size)
            pbar.console.print(f"Downloading {url} to {dst_path}")
            while data := socket.recv(block_size):
                fd.write(data)
                pbar.update(download_task, advance=len(data))
            socket.close()
            ftp.voidresp()
            ftp.quit()
        return fd.name


def download(
    url: str,
    destination: pathlib.Path,
    auth: tuple[str, str] | None = None,
    block_size: int = 1024 * 8,
) -> pathlib.Path:
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme == "ftp":
        tmp_path = download_ftplib(url=url, destination=destination, auth=auth, block_size=block_size)
    elif parsed_url.scheme in ("http", "https"):
        tmp_path = download_httpx(url=url, destination=destination, auth=auth)
    else:
        raise NotImplementedError(f"Don't know how to download protocol: {parsed_url.scheme}")
    return tmp_path


def get_first_timestamp(path: pathlib.Path) -> pd.Timestamp:
    with xr.open_dataset(path, engine="cfgrib", backend_kwargs={"indexpath": ""}) as ds:
        # I think that some GRIB files have a scalar value for time while
        # others have an aarray.
        # This if/else tries to handle both.
        if ds.time.shape:
            timestamp = pd.to_datetime(ds.time[0])
        else:
            timestamp = pd.to_datetime(ds.time.data)
        return timestamp


def get_grib_filename_from_timestamp(ts: pd.Timestamp) -> str:
    filename = ts.strftime("%Y%m%d.%H.uvp_72.grib")
    return filename


def get_blob_url_from_timestamp(container: str, ts: pd.Timestamp) -> str:
    filename = get_grib_filename_from_timestamp(ts=ts)
    url = f"{container}/{ts.strftime('%Y%m')}/{filename}"
    return url


def get_rpath_from_timestamp(
    timestamp: pd.Timestamp,
    base_rpath: pathlib.Path,
) -> pathlib.Path:
    rpath = base_rpath / timestamp.strftime("%Y%m%d.%H")
    return rpath


def retrieve_grib(url: str, destination: pathlib.Path, auth: tuple[str, str] | None) -> None:
    """
    Download GRIB file from `url` and save it to a temporary file in `destination`.
    Then retrieve the first timestamp from the GRIB file and rename the file accordingly.
    """

    tmp_path = download(url=url, destination=destination, auth=auth)
    timestamp = get_first_timestamp(tmp_path)
    filename = get_grib_filename_from_timestamp(timestamp)
    move(src=tmp_path, dst=destination / filename)


def create_hosts_file():
    cmd = "jaz templates/hosts.yml"
    proc = run(cmd, cwd=PLAYBOOKS, check=True)
    (PLAYBOOKS / "hosts.yml").write_text(proc.stdout)
