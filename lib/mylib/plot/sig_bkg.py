
import matplotlib.pyplot as plt

from mylib.plot.core.looks.leg import stats_legend
from mylib.plot.core.util.save import save
from mylib.util.data import approx_num_bins


def _sig(data):
    isSignal = (data["isSignal"]==1) & (data["KST0_isSignal"]==1) & (data["K_p_isSignal"]==1) & (data["pi_m_isSignal"]==1) & (data["e_p_isSignal"]==1) & (data["e_m_isSignal"]==1)
    return data[isSignal]


def _bkg(data):
    isBkg = (data["isSignal"]!=1) | (data["KST0_isSignal"]!=1) | (data["K_p_isSignal"]!=1) | (data["pi_m_isSignal"]!=1) | (data["e_p_isSignal"]!=1) | (data["e_m_isSignal"]!=1)
    return data[isBkg]


def plot_sig_bkg(data, var, title, xlabel, xlim=(None, None)):
    """
    Plot the signal distribution and the background distribution
    on the same plot.
    """
    sig = _sig(data)[var]
    bkg = _bkg(data)[var]
    
    if xlim != (None, None):
        sig = sig[(sig > xlim[0]) & (sig < xlim[1])]
        bkg = bkg[(bkg > xlim[0]) & (bkg < xlim[1])]
    
    leg_sig = stats_legend(sig, "Det. Signal")
    leg_mis = stats_legend(bkg, "Det. Background")

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
        bkg,
        label=leg_mis,
        bins=approx_num_bins(bkg),
        color="blue",
        histtype="step",
        linewidth=1,
    )

    ax.set_xlim(xlim)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    return fig, ax


def plot_deltaE(data, out_dir):
    fig, ax = plot_sig_bkg(
        data, 
        var="deltaE", 
        title=r'$\Delta E$', 
        xlabel=r'[GeV]',
        xlim=(-0.1, 0.1)
    )
    save("deltaE_sig_bkg", q_squared_split='all', out_dir=out_dir)


def plot_Mbc(data, out_dir):
    fig, ax = plot_sig_bkg(
        data,
        var="Mbc",
        title=r"$M_{bc}$",
        xlabel=r"[GeV]",
        xlim=(5.26, 5.30)
    )
    save("Mbc_sig_bkg", q_squared_split='all', out_dir=out_dir)


def plot_invM(data, out_dir):
    fig, ax = plot_sig_bkg(
        data,
        var="invM_K_pi_shifted",
        title=r"$M_{K, \pi} - M_{K^*}$",
        xlabel=r"[GeV]",
        xlim=(-0.2, 0.2)
    )
    save("invM_sig_bkg", q_squared_split='all', out_dir=out_dir)


def plot_q_squared(data, out_dir):
    fig, ax = plot_sig_bkg(
        data,
        var="q_squared",
        title=r"$q^2$",
        xlabel="[GeV$^2$]",
        xlim=(0,20)
    )
    save("hist_q_squared", q_squared_split='all', out_dir=out_dir)



