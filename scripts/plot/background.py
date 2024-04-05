
import pathlib as pl

import pandas as pd
from mylib.plot.lib import plot_sig_noise, setup_mpl_params_save
from mylib.util import open_data, section


setup_mpl_params_save()


data_gen_mix_mc = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-30_bdt_15i/e/charge/an')#.loc["det"][:20_000]
data_sig_mc = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-30_bdt_15i/e/signal/an')#.loc["det"][:20_000]

data_bkg_mix = section(data_gen_mix_mc, sig_noise='noise', gen_det='det')
data_sig = section(data_sig_mc, sig_noise='sig', gen_det='det')[:2_000]

data = pd.concat([data_bkg_mix, data_sig])

out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-03-30_bdt_15i/e/plots/bkg_charged')
out_dir.mkdir(parents=True, exist_ok=True)


plot_sig_noise(
    data=data,
    var='q_squared',
    q_squared_split='all',
    noise_type='both',
    title=r"$q^2$",
    xlabel="[GeV$^2$]",
    xlim=(0,20),
    ymax=9_000,
    scale='linear',
    extra_name='charge_lin',
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
    ymax=9_000,
    scale='log',
    extra_name='charge_log',
    out_dir=out_dir
)
