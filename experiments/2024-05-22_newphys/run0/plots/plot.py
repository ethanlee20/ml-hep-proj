
from math import pi
import pathlib as pl

from mylib.util import open_data
from mylib.plot import setup_mpl_params_save, plot_sm_np_comp, save_plot_and_clear


setup_mpl_params_save()

data_dir_path = pl.Path("/home/belle2/elee20/ml-hep-proj/experiments/2024_05_22_newphys/data")

sm_data = open_data("../data/sm_re_an.pkl")
np_data = open_data("../data/np_re_an.pkl")

title = r"($\mu$, NP: $\delta C_9 = -0.87$, All $q^2$)"
q_squared_split = "all"

fig, ax = plot_sm_np_comp(sm_data, np_data, "deltaE", q_squared_split, title, r"$\Delta E$ [GeV]", (-0.05, 0.05))
save_plot_and_clear(f"deltaE_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "Mbc", q_squared_split, title, r"$M_{bc}$ [GeV$^2$]", (5.27, 5.5))
save_plot_and_clear(f"mbc_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "q_squared", q_squared_split, title, r"$q^2$ [GeV$^2$]", (0, 20))
save_plot_and_clear(f"q_squared_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "costheta_mu", q_squared_split, title, r"$\cos\theta_\mu$", (-1, 1))
save_plot_and_clear(f"cos_theta_mu_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "costheta_K", q_squared_split, title, r"$\cos\theta_K$", (-1, 1))
save_plot_and_clear(f"cos_theta_k_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "chi", q_squared_split, title, r"$\chi$", (-2*pi, 2*pi))
save_plot_and_clear(f"chi_{q_squared_split}.png")


title = r"($\mu$, NP: $\delta C_9 = -0.87$, $ 1 < q^2 < 6 $ GeV$^2$)"
q_squared_split = "med"

fig, ax = plot_sm_np_comp(sm_data, np_data, "deltaE", q_squared_split, title, r"$\Delta E$ [GeV]", (-0.05, 0.05))
save_plot_and_clear(f"deltaE_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "Mbc", q_squared_split, title, r"$M_{bc}$ [GeV$^2$]", (5.27, 5.5))
save_plot_and_clear(f"mbc_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "q_squared", q_squared_split, title, r"$q^2$ [GeV$^2$]", (0, 20))
save_plot_and_clear(f"q_squared_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "costheta_mu", q_squared_split, title, r"$\cos\theta_\mu$", (-1, 1))
save_plot_and_clear(f"cos_theta_mu_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "costheta_K", q_squared_split, title, r"$\cos\theta_K$", (-1, 1))
save_plot_and_clear(f"cos_theta_k_{q_squared_split}.png")

fig, ax = plot_sm_np_comp(sm_data, np_data, "chi", q_squared_split, title, r"$\chi$", (-2*pi, 2*pi))
save_plot_and_clear(f"chi_{q_squared_split}.png")
