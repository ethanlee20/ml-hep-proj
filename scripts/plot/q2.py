import pathlib as pl

from mylib.plot.lib import setup_mpl_params_save, plot_resolution, plot_sig_noise
from mylib.util import open_data, section, veto_q_squared_mix_bkg

import pandas as pd


setup_mpl_params_save()


data_gen_mix_mc = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/an')
data_sig_mc = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/sig/an')

data_bkg = section(data_gen_mix_mc, sig_noise='noise').loc[["det"]][:20_000]
data_sig = section(data_sig_mc, sig_noise='sig').loc[["det"]][:20_000]

data = pd.concat([data_bkg, data_sig])

data_vetoed = veto_q_squared_mix_bkg(data)

out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/plots/')


plot_sig_noise(
    data=data,
    var='q_squared',
    q_squared_split='all',
    noise_type='both',
    title=r"$q^2$",
    xlabel="[GeV$^2$]",
    xlim=(0,20),
    scale='linear',
    extra_name='lin',
    out_dir=out_dir
)

plot_sig_noise(
    data=data,
    var='q_squared',
    q_squared_split='all',
    noise_type='both',
    title=r"$q^2$",
    xlabel="[GeV$^2$]",
    xlim=(0,20),
    scale='log',
    extra_name='log',
    out_dir=out_dir
)

plot_sig_noise(
    data=data_vetoed,
    var='q_squared',
    q_squared_split='all',
    noise_type='both',
    title=r"$q^2$",
    xlabel="[GeV$^2$]",
    xlim=(0,20),
    scale='linear',
    extra_name='lin',
    out_dir=out_dir
)

plot_sig_noise(
    data=data_vetoed,
    var='q_squared',
    q_squared_split='all',
    noise_type='both',
    title=r"$q^2$",
    xlabel="[GeV$^2$]",
    xlim=(0,20),
    scale='log',
    extra_name='log',
    out_dir=out_dir
)