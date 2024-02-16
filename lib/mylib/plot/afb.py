
import matplotlib.pyplot as plt

from mylib.util.data import section
from mylib.calc.afb import calc_afb_of_q_squared
from mylib.plot.core.util.save import save
from mylib.plot.core.looks.leg import stats_legend



def plot_afb(data, out_dir):
    d_cos_theta_mu = section(data, only_sig=True, var="costheta_mu")
    d_q_squared = section(data, only_sig=True, var="q_squared")

    num_points = 150
    gen = calc_afb_of_q_squared(d_cos_theta_mu.loc["gen"], d_q_squared.loc["gen"], num_points)
    det = calc_afb_of_q_squared(d_cos_theta_mu.loc["det"], d_q_squared.loc["det"], num_points)
    
    leg_gen = stats_legend(d_cos_theta_mu.loc["gen"], "Generator", show_mean=False, show_rms=False)
    leg_det = stats_legend(d_cos_theta_mu.loc["det"], "Detector", show_mean=False, show_rms=False)

    plt.scatter(*gen, s=2, color="red", alpha=0.6, label=leg_gen, marker="X")
    plt.scatter(*det, s=2, color="blue", alpha=0.6, label=leg_det, marker="d")
    plt.ylim(-0.3, 0.5)
    plt.xlim(0, 19) 
    plt.title(r"$A_{fb}$ for $\ell = \mu$")
    plt.xlabel(r"$q^2$ [GeV$^2$]")
    plt.ylabel(r"$A_{fb}$")

    plt.legend()

    save("afb", "all", out_dir)