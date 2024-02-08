
import pathlib as pl

from mylib.utilities.util import open_data, open_data_dir

from mylib.plotting.hist1d.theta_lab_k import hist_theta_lab_k
from mylib.plotting.hist2d.costheta_k import hist_2d_costheta_k_theta_k, hist_2d_costheta_k_p_k


data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00003_job388070872_00_cut_an.pkl')
out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/plots2/')


hist_theta_lab_k(data, out_dir)

hist_2d_costheta_k_theta_k(data, out_dir)

hist_2d_costheta_k_p_k(data, out_dir)
