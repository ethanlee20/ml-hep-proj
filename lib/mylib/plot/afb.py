
import matplotlib.pyplot as plt

from mylib.util.data import section
from mylib.calc.afb import calc_afb_of_q_squared
from mylib.plot.core.util.save import save



def plot_afb(data, out_dir):
    d_cos_theta_mu = section(data, only_sig=True, var="costheta_mu")
    d_q_squared = section(data, only_sig=True, var="q_squared")

    gen = calc_afb_of_q_squared(d_cos_theta_mu.loc["gen"], d_q_squared.loc["gen"])
    det = calc_afb_of_q_squared(d_cos_theta_mu.loc["det"], d_q_squared.loc["det"])
    
    plt.scatter(*gen, color="red", label="Generator")
    plt.scatter(*det, color="blue", label="Detector")
    plt.title(r"$A_{fb}$ for $\ell = \mu$")
    plt.xlabel(r"$q^2$ [GeV$^2$]")
    plt.ylabel(r"$A_{fb}$")

    save("afb", "all", out_dir)