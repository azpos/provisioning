#! /usr/bin/env python

from ecmwfapi import ECMWFService
import sys
import pandas as pd

date = sys.argv[1]
dstamp = pd.to_datetime(date)

day = dstamp.strftime(format='%Y-%m-%d')
s = dstamp.strftime(format='%Y%m%d.%H')

server = ECMWFService("mars")

server.execute({
    'stream'    : "oper",
    'levtype'   : "sfc",
    'param'     : "MSL/10U/10V",
    'expver'    : "1",
    'step'      : "00/TO/72/by/01",
    'area'      : "90.0/0.0/-90.0/360.0",
    'grid'      : "F1280",
    'time'      : "{:02d}".format(dstamp.hour),
    'date'      : "{}".format(day),
    'type'      : "fc",
    'class'     : "od"},
#   'format'    : "netcdf",
    "{}.uvp_72.grib".format(s)
 )
