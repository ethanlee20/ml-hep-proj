import os
import sys
import pathlib as pl

import pytest
import pandas as pd

sys.path.append(
    os.path.join(os.path.dirname(__file__), "../")
)

import plotting


plotting.setup_mpl_params_save()

data = pd.read_pickle("/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/mu_re_00000_job386260828_00_cut_an.pkl")

out_dir_path = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/plots/test')
out_dir_path.mkdir(parents=True, exist_ok=True)


def test_plot_candidate_multiplicity():
    plotting.plot_candidate_multiplicity(data, out_dir_path)



