
import pathlib as pl

import pandas as pd

import mylib


data_dir_path = pl.Path("/home/belle2/elee20/ml-hep-proj/data/2024-01-08_LargeMu_backup/")
in_file_name = "mc_re_cut_an.pkl"


plots_dir_name = "plots"
mult_plots_dir_name = "mult"
out_dir_path = data_dir_path.joinpath(plots_dir_name).joinpath(mult_plots_dir_name)
out_dir_path.mkdir(parents=True, exist_ok=True)

in_file_path = data_dir_path.joinpath(in_file_name)

data = pd.read_pickle(in_file_path).loc["det"]
label = "detector level (cut)"
mylib.plot_candidate_multiplicity(data, label, out_dir_path)
