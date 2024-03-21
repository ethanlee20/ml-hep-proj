
import pathlib as pl

from mylib.util.util import open_data

from mylib.plot.core.util.setup import setup_mpl_params_save

from mylib.plot.sig_bkg import (
    plot_deltaE,
    plot_mbc,
    plot_invM,
    plot_q_squared
)



setup_mpl_params_save()

data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/an')

out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/plots/')
