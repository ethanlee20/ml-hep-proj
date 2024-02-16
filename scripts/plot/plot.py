
import pathlib as pl

from mylib.util.util import open_data, open_data_dir

from mylib.plot.core.util.setup import setup_mpl_params_save

from mylib.plot.hist_1d.theta_lab_k import hist_theta_lab_k

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

data = open_data_dir('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/')
# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00003_job388070872_00_cut_an.pkl')
out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/plots2/')


hist_theta_lab_k(data, out_dir)

# hist_2d_costheta_k_theta_k(data, out_dir)
# hist_2d_costheta_k_p_k(data, out_dir)

# hist_2d_chi_p_k(data, out_dir)
# hist_2d_chi_theta_k(data, out_dir)

# eff_cos_theta_k(data, out_dir)
# eff_cos_theta_k_check_theta_k_accep(data, out_dir)


