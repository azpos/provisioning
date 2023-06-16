from __future__ import annotations

import pathlib

import eliot.json
import pandas as pd


class MyEncoder(eliot.json.EliotJSONEncoder):
    def default(self, obj):
        if isinstance(obj, (pd.Timestamp, pathlib.Path)):
            return str(obj)
        return eliot.json.EliotJSONEncoder.default(self, obj)


eliot.to_file(open("linkcheck.log", "w"), encoder=MyEncoder)
