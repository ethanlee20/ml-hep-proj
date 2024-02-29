
import pathlib as pl

from mylib.util.util import open_data, open_data_dir

from mylib.plot.core.util.setup import setup_mpl_params_save

from mylib.plot.hist_1d.gen_det.chi import hist_chi
from mylib.plot.hist_1d.gen_det.costheta_K import hist_costheta_K
from mylib.plot.hist_1d.gen_det.costheta_e import hist_costheta_e
from mylib.plot.hist_1d.gen_det.q_squared import hist_q_squared
from mylib.plot.hist_1d.gen_det.theta_lab_k import hist_theta_lab_k

from mylib.plot.hist_1d.sig_mis.sig_mis import plot_deltaE, plot_invM, plot_mbc
from mylib.plot.hist_2d.deltaE_Mbc import hist2d_deltaE_mbc

# from mylib.plot.afb import plot_afb
# from mylib.plot.s5 import plot_s5



# from mylib.plot.hist2d.costheta_k import (
#     hist_2d_costheta_k_theta_k, 
#     hist_2d_costheta_k_p_k, 
# )

# from mylib.plotting.hist2d.chi import (
#     hist_2d_chi_p_k, 
#     hist_2d_chi_theta_k
# )

# from mylib.plotting.efficiency.costheta_k import (
#     eff_cos_theta_k, 
#     eff_cos_theta_k_check_theta_k_accep,
# )


setup_mpl_params_save()

# data = open_data_dir('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/mc/BtoKstee2/sub00', tree_names=['gen', 'det'])
data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/mc/BtoKstee2/sub00/e_re_00051_job394437823_00.root', tree_names=['gen', 'det'])
# data = open_data_dir('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/')
# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00003_job388070872_00_cut_an.pkl')
out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/plots_uncut')


plot_deltaE(data, out_dir)
# plot_mbc(data, out_dir)
# plot_invM(data, out_dir)
# hist2d_deltaE_mbc(data, out_dir)

# hist_chi(data, out_dir)
# hist_costheta_e(data, out_dir)
# hist_costheta_K(data, out_dir)
# hist_q_squared(data, out_dir)

# hist_theta_lab_k(data, out_dir)

# plot_afb(data, out_dir)
# plot_s5(data, out_dir)
# hist_2d_costheta_k_theta_k(data, out_dir)
# hist_2d_costheta_k_p_k(data, out_dir)

# hist_2d_chi_p_k(data, out_dir)
# hist_2d_chi_theta_k(data, out_dir)

# eff_cos_theta_k(data, out_dir)
# eff_cos_theta_k_check_theta_k_accep(data, out_dir)


