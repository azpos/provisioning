from __future__ import annotations

import os
import pathlib
import shutil
import typing as T

import natsort
import pandas as pd
import pyposeidon.model as pmodel
import pyposeidon.schism as pschism
import pyposeidon.tools as ptools
import pyposeidon.utils.cast as pcast
import rich
import typer
import xarray as xr

from seareport import tools


def get_model_definition(
    base_model: pathlib.path, base_rpath: pathlib.path, meteo_file: pathlib.Path
) -> dict[str : T.Any]:
    timestamp = tools.get_first_timestamp(meteo_file)
    model_definition = {
        "solver_name": "schism",
        "mesh_file": str(base_model / "hgrid.gr3"),
        "start_date": timestamp,
        "time_frame": "72H",
        "meteo_source": [str(meteo_file)],
        "update": ["model", "meteo"],
        "rpath": str(tools.get_rpath_from_timestamp(base_rpath=base_rpath, timestamp=timestamp)),
        "meteo_split_by": "day",
        "parameters": {
            "dt": 150,
            "rnday": 3.0,
            "nhot": 1,
            "ihot": 0,
            "nspool": 24,
            "ihfskip": 96,
            "nhot_write": 288,
            "wtiminc": 3600,
        },
    }
    return model_definition


def gen_initial(
    base_model: pathlib.Path,
    base_rpath: pathlib.Path,
    meteo_file: pathlib.Path,
) -> None:
    model_definition = get_model_definition(
        base_model=base_model,
        base_rpath=base_rpath,
        meteo_file=meteo_file,
    )
    model = pmodel.set(**model_definition)
    model.create()  # constructs all required parts e.g. mesh, dem, meteo, etc.
    model.output()  # save to files
    model.save()  # saves the json model reference file
    model.set_obs()  # setup station points
    # Explicitly copy the launchSchism.sh from the base_model
    shutil.copy2(base_model / "launchSchism.sh", model.rpath)
    return model



def gen_next(
    base_model: pathlib.Path,
    base_rpath: pathlib.Path,
    meteo_file: pathlib.Path,
) -> None:
    current_timestamp = tools.get_first_timestamp(meteo_file)
    current_rpath = tools.get_rpath_from_timestamp(base_rpath=base_rpath, timestamp=current_timestamp)
    previous_timestamp = current_timestamp - pd.DateOffset(hours=12)
    previous_rpath = tools.get_rpath_from_timestamp(base_rpath=base_rpath, timestamp=previous_timestamp)

    # the base_rpath should contain a tar.zst with the packed results of the previous run. Unpack it in base_rpath
    previous_archive = base_rpath / f"{previous_rpath.name}.tar.zst"
    if not previous_archive.exists():
        rich.print(f"\n[bold red]Archive of previous run is missing: {str(previous_archive)}")
        rich.print("\n[bold red]Download it and try again!")
        raise typer.Abort()
    with tools.cli_log(f"Unpacking previous model: {str(previous_archive)}", "Unpacking: Successful!"):
        tools.run_cli(cmd=f"tar xvf {previous_archive}", cwd=base_rpath, show_output=True, show_traceback=True)
        # sanity check
        if not (previous_rpath.exists() and previous_rpath.is_dir()):
            raise ValueError(f"missing previous rpath: {previous_rpath}")

    with tools.cli_log(f"Copying base model to previous model: {str(previous_rpath)}", "Copying of base model: Successful!"):
        shutil.copytree(base_model, previous_rpath, dirs_exist_ok=True)

    with tools.cli_log("Calling cast", "Cast: Successful!"):
        previous_model = pmodel.read(str(previous_rpath / "schism_model.json"))
        next_model_cast = pcast.set(
            solver_name="schism",
            model=previous_model,  # reference model
            ppath=previous_model.rpath,  # original path
            cpath=str(current_rpath),  # new path
            meteo=str(meteo_file),  # new meteo
            sdate=current_timestamp,  # new start time
            copy=True,  # optional, default is simlink for common files
        )
        next_model_cast.run(execute=False)


_TO_BE_PACKED = [
    "outputs/mirror.out",
    "outputs/flux.out",
    "outputs/staout_1",
    "outputs/staout_2",
    "outputs/staout_3",
    "outputs/staout_4",
    "outputs/staout_5",
    "outputs/staout_6",
    "outputs/staout_7",
    "outputs/staout_8",
    "outputs/staout_9",
    "param.nml",
    "schism_model.json",
    "sflux/sflux_inputs.txt",
]


def pack_model(model_rpath: pathlib.Path, hotstart_file: pathlib.Path) -> pathlib.Path:
    base_rpath = model_rpath.parent
    archive_path = base_rpath / f"{model_rpath.name}.tar.zst"
    rich.print(f"\n[italic yellow]Packing model output to: {str(archive_path)}")
    files = [str((model_rpath / file).relative_to(base_rpath)) for file in _TO_BE_PACKED + [hotstart_file]]
    rich.print("\n[italic yellow]Files to be packed:\n")
    for file in files:
        rich.print(f"[bold]{file}[bold]")
    cmd = f"time tar -C {str(model_rpath.parent)} -c -I 'zstd -3 -T0' -f {str(archive_path)} {' '.join(files)}"
    tools.run_cli(cmd=cmd, show_traceback=True, show_output=False)
    return archive_path


def merge_results(model_rpath: pathlib.Path) -> pathlib.Path:
    output_netcdf = model_rpath.parent / f"{model_rpath.name}.nc"
    rich.print(f"\n[italic yellow]Merging model output to: {str(output_netcdf)}")
    to_be_merged = natsort.natsorted(
        set(model_rpath.glob("outputs/schout*.nc")) - set(model_rpath.glob("outputs/schout_*_*.nc"))
    )
    if not to_be_merged:
        rich.print("\n[bold red]No files to merge!")
        rich.print(f"[bold red]Check the outputs directory at: {str(model_rpath / 'outputs')}")
        raise typer.Abort()

    rich.print("\n[italic yellow]Files to be merged:\n")
    for file in to_be_merged:
        rich.print(f"[bold]{file}[bold]")
    print()
    ds = xr.open_mfdataset(to_be_merged, data_vars="minimal", parallel=True)
    #ds = ptools.merge_netcdfs(to_be_merged, max_size=3)
    rich.print("\n[italic bold green]Merge operation: Successful!")
    ds["max_elev"] = ds.elev.max("time")
    rich.print("\n[italic bold green]Max elevation calculation: Successful!")
    # Compress variables and chunk along time
    encoding = {}
    for var in ds.data_vars:
        nc_chunksizes = dict(ds[var].sizes)
        if "time" in nc_chunksizes:
            nc_chunksizes["time"] = 1
        encoding[var] = dict(zlib=True, complevel=1, chunksizes=list(nc_chunksizes.values()))
    ds.to_netcdf(output_netcdf, encoding=encoding)
    rich.print("\n[italic bold green]Writing output to disk: Successful!")
    return output_netcdf


def compress_staout(model_rpath: pathlib.Path) -> pathlib.Path:
    with tools.cli_log("Compressing staout", "Compression: Successful!"):
        archive_name = shutil.make_archive(
            base_name=f"{model_rpath.name}.staout_1",
            format="zip",
            root_dir=model_rpath / "outputs",
            base_dir="staout_1"
        )
        return archive_name

def calc_hotstart(model: pschism.Schism) -> pathlib.Path:
    dt = int(model.params["core"]["dt"])
    hotout = int((model.start_date + pd.DateOffset(hours=12) - pd.to_datetime(model.rdate)).total_seconds() / dt)
    hotstart_file = os.path.join(model.rpath, f"outputs/hotstart_it={hotout}.nc")
    with tools.cli_log(f"Calculating hotstart: {hotstart_file}", "Hotstart calculation: Successful!"):
        model.hotstart(it=hotout)
    with tools.cli_log("Compressing staout", "Compression: Successful!"):
        compress_staout(pathlib.Path(model.rpath))
    return hotstart_file


def post_process(model_rpath: pathlib.Path) -> None:
    model = pmodel.read(str(model_rpath / "schism_model.json"))
    model.results()  # create intermediate results
    merge_results(model_rpath)
    hotstart_file = calc_hotstart(model)
    pack_model(model_rpath, hotstart_file)


def run_model(model_rpath: pathlib.Path) -> None:
    cmd = str(model_rpath / "launchSchism.sh")
    tools.run_cli(cmd, show_traceback=True, show_output=True)


def run_model_ssh(model_rpath: pathlib.Path) -> None:
    shared = pathlib.Path("/scratch/shared/rpath")
    with tools.cli_log("Copying from control to cluster", "Copy: Successful!"):
        cmd = f"cp -r {model_rpath} {shared}"
        tools.run_cli(cmd=cmd, show_output=True, show_traceback=True)
    with tools.cli_log("Executing model", "Model execution: Successful!"):
        cmd = """ssh 10.10.0.5 -t 'bash -li -c "/scratch/shared/rpath/launchSchism.sh"'"""
        tools.run_cli(cmd=cmd, show_output=True, show_traceback=True)
    with tools.cli_log("Copying from cluster to control", "Copy: Successful!"):
        shutil.copytree(shared / "outputs", model_rpath / "outputs")
