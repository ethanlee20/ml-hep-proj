
import pathlib as pl

import pandas as pd

from mylib.plot.lib import plot_hist, setup_mpl_params_save

from mylib.util import open_data, section


setup_mpl_params_save()


data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-05-03_sig_e/e_sig_single4/sub00')
data = section(data, gen_det='det')
isSignal = (data['e_m_isSignalAcceptBremsPhotons']==1) & (data['e_p_isSignalAcceptBremsPhotons']==1) & (data['pi_m_isSignalAcceptBremsPhotons']==1) & (data['K_p_isSignalAcceptBremsPhotons']==1) & (data['KST0_isSignalAcceptBremsPhotons']==1)
data = data[isSignal]

plot_dir_path = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-05-03_sig_e/e_sig_single4/plots')
plot_dir_path.mkdir(parents=True, exist_ok=True)


# plot_hist(
#     data["vpho_tfRedChiSqVpho"],
#     title=r"$\chi^2_\text{red}$ dilepton",
#     xlabel='',
#     xlim=(0, 20),
#     save_path=plot_dir_path.joinpath('tfredchisqvpho.png')
# )

# plot_hist(
#     data["tfRedChiSqB0"],
#     title=r"$\chi^2_\text{red}$ $B^0$",
#     xlabel='',
#     xlim=(0,20),
#     save_path=plot_dir_path.joinpath('tfredchisqb0.png')
# )

plot_hist(
    data["CMS3_weMissM2"],
    title=r"$M_\text{miss}^2$",
    xlabel='[GeV$^2$]',
    xlim=(-0.5,0.1),
    save_path=plot_dir_path.joinpath('mmisssq.png')
)
