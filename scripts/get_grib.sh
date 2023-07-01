#!/usr/bin/env bash
#

set -euo pipefail

base_url=https://jeodpp.jrc.ec.europa.eu/ftp/private/zyWUYa4wk/nxGGjsuRHYrOuTx1/output-ftp/ECMWF/Operational/HRES/LATEST/Data/GRIB

for year in 2023; do
  for month in 06; do
    # for day in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do
    for day in 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do
      for hour in 00 12; do
        filename="${year}""${month}""${day}"."${hour}".uvp_72.grib;
        echo "${filename}";
        wget -q "${base_url}"/"${year}"/"${month}"/"${day}"/"${year}""${month}""${day}"."${hour}".uvp_72.grib;
        azcopy copy --overwrite true "${filename}" https://ppwdevarchivecoolsa.blob.core.windows.net/ecmwf/"${year}""${month}"/"${filename}";
        rm -rf "${filename}";
        ntfy send "${filename}"
      done;
    done;
  done;
done;
