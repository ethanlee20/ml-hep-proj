
import pathlib as pl

from mylib.util.util import open_data, open_data_dir

from mylib.plot.core.util.setup import setup_mpl_params_save

# from mylib.plot.hist_1d.gen_det.chi import hist_chi
# from mylib.plot.hist_1d.gen_det.costheta_K import hist_costheta_K
# from mylib.plot.hist_1d.gen_det.costheta_e import hist_costheta_e
# from mylib.plot.hist_1d.gen_det.q_squared import hist_q_squared
# from mylib.plot.hist_1d.gen_det.theta_lab_k import hist_theta_lab_k

# from mylib.plot.hist_1d.basic import plot_deltaE, plot_mbc, plot_invM
# from mylib.plot.hist_1d.ang import hist_chi, hist_costheta_e, hist_costheta_K, hist_q_squared
# from mylib.plot.eff import eff_chi, eff_cos_theta_e, eff_cos_theta_k

# from mylib.plot.hist_2d.deltaE_Mbc import hist2d_deltaE_mbc

# from mylib.plot.afb import plot_afb
# from mylib.plot.s5 import plot_s5

# from mylib.plot.cand_mult import plot_candidate_multiplicity
from mylib.plot.core.hist_2d.deltaE_Mbc import hist2d_deltaE_mbc


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
# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/cut/e_re_00051_job394437823_00_cut.pkl', tree_names=['gen', 'det'])
# data = open_data_dir('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/')
# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00003_job388070872_00_cut_an.pkl')
# data = open_data_dir('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/ana', tree_names=['gen', 'det'])
# data = open_data_dir('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/subset/mc', tree_names=['gen', 'det'])
data = open_data_dir('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/subset/cut', tree_names=['gen', 'det'])

# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/ana/e_re_00051_job394437823_00_cut_an.pkl', tree_names=['gen', 'det'])

# out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/subset/plots/')
out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-02-29_eGrid/subset/plots/')


hist2d_deltaE_mbc(data, out_dir, sig_only=True)

# plot_candidate_multiplicity(data, out_dir, ell='e')



# plot_deltaE(data, out_dir)
# plot_mbc(data, out_dir)
# plot_invM(data, out_dir)
# eff_cos_theta_k(data, out_dir)
# eff_cos_theta_e(data, out_dir)
# eff_chi(data, out_dir)

# hist2d_deltaE_mbc(data, out_dir)

# hist_chi(data, out_dir)
# hist_costheta_e(data, out_dir)
# hist_costheta_K(data, out_dir)
# hist_q_squared(data, out_dir)

# hist_theta_lab_k(data, out_dir)

# plot_afb(data, out_dir, ell='e')
# plot_s5(data, out_dir, ell='e')
# hist_2d_costheta_k_theta_k(data, out_dir)
# hist_2d_costheta_k_p_k(data, out_dir)

# hist_2d_chi_p_k(data, out_dir)
# hist_2d_chi_theta_k(data, out_dir)

# eff_cos_theta_k(data, out_dir)
# eff_cos_theta_k_check_theta_k_accep(data, out_dir)


