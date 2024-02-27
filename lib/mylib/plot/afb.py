
import matplotlib.pyplot as plt

from mylib.util.data import section
from mylib.calc.afb import calc_afb_of_q_squared
from mylib.plot.core.util.save import save
from mylib.plot.core.looks.leg import stats_legend



def plot_afb(data, out_dir):
    d_cos_theta_mu = section(data, only_sig=True, var="costheta_mu")
    d_q_squared = section(data, only_sig=True, var="q_squared")

    num_points = 150
    gen_x, gen_y, gen_err = calc_afb_of_q_squared(d_cos_theta_mu.loc["gen"], d_q_squared.loc["gen"], num_points)
    det_x, det_y, det_err = calc_afb_of_q_squared(d_cos_theta_mu.loc["det"], d_q_squared.loc["det"], num_points)
    # breakpoint()
    leg_gen = stats_legend(d_cos_theta_mu.loc["gen"], "Generator", show_mean=False, show_rms=False)
    leg_det = stats_legend(d_cos_theta_mu.loc["det"], "Detector", show_mean=False, show_rms=False)

    plt.errorbar(gen_x, gen_y, yerr=gen_err, fmt='none', ecolor='red', elinewidth=0.5, capsize=1, alpha=0.7)
    plt.scatter(gen_x, gen_y, s=4, color="red", alpha=0.7, label=leg_gen, marker="X")
    plt.errorbar(det_x, det_y, yerr=det_err, fmt='none', ecolor='blue', elinewidth=0.5, capsize=1, alpha=0.7)
    plt.scatter(det_x, det_y, s=4, color="blue", alpha=1, label=leg_det, marker="d", alpha=0.7)
    plt.ylim(-0.3, 0.5)
    plt.xlim(0, 19) 
    plt.title(r"$A_{FB}$ for $\ell = \mu$")
    plt.xlabel(r"$q^2$ [GeV$^2$]")
    plt.ylabel(r"$A_{FB}$")

    plt.legend()

    save("afb", "all", out_dir)