import pathlib as pl

from mylib.plot.lib import setup_mpl_params_save, plot_resolution, plot_sig_noise
from mylib.util import open_data, section, veto_q_squared_mix_bkg

import pandas as pd


setup_mpl_params_save()

data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/sig/an')

out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/plots/res')
out_dir.mkdir(parents=True, exist_ok=True)


plot_resolution(
    data,
    variable='q_squared',
    q_squared_split='all',
    title=r'Resolution of $q^2$ (all $q^2$)',
    xlabel=r'q^2_\text{recon} - q^2_\text{mc truth}',
    xlim=(-1,1),
    extra_name=''
)

plot_resolution(
    data,
    variable='q_squared',
    q_squared_split='J/psi',
    title=r'Resolution of $q^2$ ($8 < q^2 < 11$ GeV$^2$)',
    xlabel=r'q^2_\text{recon} - q^2_\text{mc truth}',
    xlim=(-1,1),
    extra_name=''
)