
"""Convert all root files to pickle files (given a directory)."""

import sys
import os
import pathlib as pl

from  mylib.util.util import open_data


def config_paths(input_dir):
    input_dir = pl.Path(input_dir)
    input_paths = list(input_dir.glob("*.root"))

    output_paths = [
        input_dir.joinpath(path.stem + '.pkl')
        for path in input_paths
    ]

    return input_paths, output_paths


def convert(input_path, output_path):
    data = open_data(input_path)
    data.to_pickle(output_path)
    os.remove(input_path)
    


dir_path = sys.argv[1]

input_paths, output_paths = config_paths(dir_path)

for in_path, out_path in zip(input_paths, output_paths):
    convert(in_path, out_path)