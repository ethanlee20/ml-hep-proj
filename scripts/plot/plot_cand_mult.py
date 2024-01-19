
import pathlib as pl

import pandas as pd

import mylib

mylib.setup_mpl_params_save()

data_dir_path = pl.Path("/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/")

data_to_plot_dir_path = data_dir_path.joinpath("analyzed/")

mylib.plot_candidate_multiplicity(
    data=mylib.open_dir(data_to_plot_dir_path),  
    out_dir_path=data_dir_path.joinpath('plots/')
)
