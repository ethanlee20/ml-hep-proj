import pathlib as pl

from mylib.plot.lib import setup_mpl_params_save, plot_resolution, plot_sig_noise
from mylib.util import open_data, section, veto_q_squared

import pandas as pd


setup_mpl_params_save()

# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/sig/an')
data = open_data("/home/belle2/elee20/ml-hep-proj/data/2024-03-30_bdt_15i/mu/signal/an")

out_dir = pl.Path("/home/belle2/elee20/ml-hep-proj/data/2024-03-30_bdt_15i/mu/plots")
out_dir.mkdir(parents=True, exist_ok=True)

plot_sig_noise(
    data=data,
    var='q_squared',
    q_squared_split='all',
    noise_type='mis',
    title=r"$q^2$",
    xlabel="[GeV$^2$]",
    xlim=(0,20),
    ymax=None,
    scale='linear',
    extra_name='',
    out_dir=out_dir
)

plot_resolution(
    data,
    variable='q_squared',
    q_squared_split='all',
    title=r'Resolution of $q^2$ \large (all $q^2$)',
    xlabel=r'$q^2_\text{recon} - q^2_\text{mc truth}$ [GeV$^2$]',
    xlim=(-1,1),
    extra_name='',
    out_dir_path=out_dir
)

plot_resolution(
    data,
    variable='q_squared',
    q_squared_split='JPsi',
    title=r'Resolution of $q^2$ \large ($8 < q^2 < 11$ GeV$^2$)',
    xlabel=r'$q^2_\text{recon} - q^2_\text{mc truth}$ [GeV$^2$]',
    xlim=(-1,1),
    extra_name='',
    out_dir_path=out_dir
)