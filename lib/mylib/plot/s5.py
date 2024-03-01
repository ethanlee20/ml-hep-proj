
import matplotlib.pyplot as plt

from mylib.util.data import section
from mylib.calc.s5 import calc_s5_of_q_squared
from mylib.plot.core.util.save import save
from mylib.plot.core.looks.leg import stats_legend


def plot_s5(df, out_dir, ell):
    df = section(df, only_sig=True)
    # df = df[df["mcPDG"] == 511]

    num_points = 150
    gen_x, gen_y, gen_err = calc_s5_of_q_squared(df.loc["gen"], num_points)
    det_x, det_y, det_err = calc_s5_of_q_squared(df.loc["det"], num_points)
    # breakpoint()
    
    leg_gen = stats_legend(df["chi"].loc["gen"], "Generator", show_mean=False, show_rms=False)
    leg_det = stats_legend(df["chi"].loc["det"], "Detector", show_mean=False, show_rms=False)

    plt.errorbar(gen_x, gen_y, yerr=gen_err, fmt='none', ecolor='red', elinewidth=0.5, capsize=1, alpha=0.7)
    plt.scatter(gen_x, gen_y, s=4, color="red", alpha=0.7, label=leg_gen, marker="X")
    plt.errorbar(det_x, det_y, yerr=det_err, fmt='none', ecolor='blue', elinewidth=0.5, capsize=1, alpha=0.7)
    plt.scatter(det_x, det_y, s=4, color="blue", alpha=0.7, label=leg_det, marker="d")

    plt.ylim(-0.5, 0.35)
    plt.xlim(0, 19) 
    if ell == 'e':
        plt.title(r"$S_5$ for $\ell = e$")
    elif ell == 'mu':
        plt.title(r"$S_5$ for $\ell = \mu$")
    plt.xlabel(r"$q^2$ [GeV$^2$]")
    plt.ylabel(r"$S_5$")

    plt.legend()

    save("s5", "all", out_dir)