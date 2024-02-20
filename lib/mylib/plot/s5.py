
import matplotlib.pyplot as plt

from mylib.util.data import section
from mylib.calc.s5 import calc_s5_of_q_squared
from mylib.plot.core.util.save import save
from mylib.plot.core.looks.leg import stats_legend


def plot_s5(df, out_dir):
    df = section(df, only_sig=True)

    num_points = 30
    gen_q_sq, gen_s5 = calc_s5_of_q_squared(df.loc["gen"], num_points)
    det_q_sq, det_s5 = calc_s5_of_q_squared(df.loc["det"], num_points)
    
    leg_gen = stats_legend(gen_s5, "Generator", show_mean=False, show_rms=False)
    leg_det = stats_legend(det_s5, "Detector", show_mean=False, show_rms=False)

    plt.scatter(gen_q_sq, gen_s5, s=4, color="red", alpha=0.6, label=leg_gen, marker="X")
    plt.scatter(det_q_sq, det_s5, s=4, color="blue", alpha=0.6, label=leg_det, marker="d")
    # plt.ylim(-0.3, 0.5)
    # plt.xlim(0, 19) 
    plt.title(r"$S_5$ for $\ell = \mu$")
    plt.xlabel(r"$q^2$ [GeV$^2$]")
    plt.ylabel(r"$S_5$")

    plt.legend()

    save("s5", "all", out_dir)