import sys
import pathlib as pl

import numpy as np
import pandas as pd

from mylib.util.util import open_data
from mylib.pre.cuts import apply_all_cuts_with_counts    


def config_input_data_paths(input_dir):
    input_dir = pl.Path(input_dir)
    input_paths = list(input_dir.glob("*.root"))
    return input_paths


def config_output_data_paths(output_dir, input_paths):    
    output_dir = pl.Path(output_dir)
    output_paths = [
        output_dir.joinpath(f"{path.stem}_cut.pkl")
        for path in input_paths
    ]
    return output_paths


def config_paths(input_dir, output_dir):
    input_paths = config_input_data_paths(input_dir)
    output_paths = config_output_data_paths(output_dir, input_paths)
    return input_paths, output_paths


def apply_cuts(df):
    df_gen_uncut = df.loc['gen']
    df_det_cut, counts = apply_all_cuts_with_counts(
        df.loc['det'],
    )
    cut_df = pd.concat([df_gen_uncut, df_det_cut], keys=['gen', 'det'])
    return cut_df, counts


input_dir = '/home/belle2/elee20/ml-hep-proj/data/2024-02-23_e_brems_test/recon'
output_dir = '/home/belle2/elee20/ml-hep-proj/data/2024-02-23_e_brems_test/cut'

input_paths, output_paths = config_paths(input_dir, output_dir)

tot_counts = pd.DataFrame({"sig":np.zeros(4), "mis":np.zeros(4)})

for in_path, out_path in zip(input_paths, output_paths):
    df = open_data(in_path, tree_names=['gen', 'det'])
    cut_df, counts = apply_cuts(df)
    cut_df.to_pickle(out_path)
    tot_counts += counts

np.savetxt(f'{output_dir}/flow.txt', tot_counts, fmt="%i")


