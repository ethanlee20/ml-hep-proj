
import matplotlib.pyplot as plt

from mylib.plot.core.looks.leg import stats_legend
from mylib.util import save_plot
from mylib.util import (
    approx_num_bins,
    sig_,
    noise_
)


def _plot_sig_noise(data, var, noise_type, title, xlabel, xlim=(None, None)):
    """
    Plot the signal distribution and the noise distribution
    on the same plot.
    """
    sig = sig_(data)[var]
    noise = noise_(data)[var]
    
    if xlim not in {(None, None), None}:
        sig = sig[(sig > xlim[0]) & (sig < xlim[1])]
        noise = noise[(noise > xlim[0]) & (noise < xlim[1])]
    
    leg_sig = stats_legend(sig, "Det. Signal")
    if noise_type == 'bkg':
        leg_noise = stats_legend(noise, "Det. Background")
    elif noise_type == 'mis':
        leg_noise = stats_legend(noise, "Det. Misrecon.", show_mean=False, show_rms=False)
    elif noise_type == 'both':
        leg_noise = stats_legend(noise, "Det. Bkg./Misrecon.")


    fig, ax = plt.subplots()

    ax.hist(
        sig,
        label=leg_sig,
        bins=approx_num_bins(sig),
        alpha=0.6,
        color="red",
        histtype="stepfilled",
    )

    ax.hist(
        noise,
        label=leg_noise,
        bins=approx_num_bins(noise),
        color="blue",
        histtype="step",
        linewidth=1,
    )

    ax.set_xlim(xlim)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    return fig, ax


def plot_deltaE(data, noise_type, out_dir, name="deltaE_sig_noise", xlim=(-0.1,0.1)):
    fig, ax = _plot_sig_noise(
        data, 
        var="deltaE", 
        noise_type=noise_type,
        title=r'$\Delta E$', 
        xlabel=r'[GeV]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_Mbc(data, noise_type, out_dir, name="Mbc_sig_noise", xlim=(5.26, 5.30)):
    fig, ax = _plot_sig_noise(
        data, 
        var="Mbc",
        noise_type=noise_type,
        title=r"$M_{bc}$",
        xlabel=r'[GeV]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_invM(data, noise_type, out_dir, name="invM_sig_noise", xlim=(-0.2, 0.2)):
    fig, ax = _plot_sig_noise(
        data, 
        var="invM_K_pi_shifted",
        noise_type=noise_type,
        title=r"$M_{K, \pi} - M_{K^*}$",
        xlabel=r'[GeV]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_q_squared(data, noise_type, out_dir, name="q_sq_sig_noise", xlim=(0,20)):
    fig, ax = _plot_sig_noise(
        data, 
        var="q_squared",
        noise_type=noise_type,
        title=r"$q^2$",
        xlabel=r'[GeV$^2$]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_tf_red_chi_sq(data, noise_type, out_dir, name="tf_red_chi_sq_sig_noise", xlim=(0,10)):
    fig, ax = _plot_sig_noise(
        data, 
        var="tfRedChiSq",
        noise_type=noise_type,
        title=r"$\chi^2_\textrm{red}$",
        xlabel=r"",
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)



