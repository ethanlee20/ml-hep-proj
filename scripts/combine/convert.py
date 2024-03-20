
import os
import sys
import pathlib as pl

import pandas as pd

from  mylib.util.util import open_data


def config_paths(input_dir):
    input_dir = pl.Path(input_dir)
    input_paths = list(input_dir.glob("*.pkl")) + list(input_dir.glob("*.root"))

    output_paths = input_paths.copy()
    for output_path in output_paths:
        output_path.suffix = ".pkl"

    return input_paths, output_paths


def convert(input_path, output_path):
    data = open_data(input_path)
    data.to_pickle(output_path)
    os.remove(input_path)
    


dir_path = '/home/belle2/elee20/ml-hep-proj/data/2024-03-20_gen_mix_e_new_cuts_test/gen_mix_e_new_cuts_test/sub00'

input_paths, output_paths = config_paths(dir_path)

for in_path, out_path in zip(input_paths, output_paths):
    convert(in_path, out_path)