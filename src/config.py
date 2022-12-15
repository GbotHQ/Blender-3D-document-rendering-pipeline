from typing import Iterable
import json

from pathlib import Path as pth

conf_path = pth("conf.json")
# make sure to look for config file in project root instead of src
if pth.cwd().stem == "src":
    conf_path = pth("..", conf_path)


def read():
    with open(conf_path) as json_file:
        data = json.load(json_file)
    return data["samples"]


def write(samples: Iterable[dict]):
    with open(conf_path, "w") as json_file:
        json.dump({"samples": tuple(samples)}, json_file, indent=4)
