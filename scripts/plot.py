
import pathlib as pl

import pandas as pd

from mylib.util.util import open_data
from mylib.plot.core.util.setup import setup_mpl_params_save

from mylib.plot.sig_bkg import (
    plot_deltaE,
    plot_Mbc,
    plot_invM,
    plot_q_squared,
    plot_tf_red_chi_squared
)



setup_mpl_params_save()



def _sig(data):
    isSignal = data["isSignal"]==1
    return data[isSignal]

def _bkg(data):
    isBkg = data["isSignal"]!=1
    return data[isBkg]


data_bkg_mix = _bkg(open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/an')).loc["det"][:20_000]
data_sig = _sig(open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/sig/an')).loc["det"][:20_000]

data = pd.concat([data_bkg_mix, data_sig])

def veto_q_squared(data):
    veto_j_psi = ~((data['q_squared'] > 9) & (data['q_squared'] < 10)) 
    data = data[veto_j_psi]
    veto_psi_2s = ~((data['q_squared'] > 12.75) & (data['q_squared'] < 14))
    data = data[veto_psi_2s]
    return data

data = veto_q_squared(data)

out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/plots/')

# plot_deltaE(data, out_dir)
# plot_invM(data, out_dir)
# plot_Mbc(data, out_dir)
plot_q_squared(data, out_dir)
# plot_tf_red_chi_squared(data, out_dir)


