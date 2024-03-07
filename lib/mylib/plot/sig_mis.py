
import matplotlib.pyplot as plt

from mylib.plot.core.looks.leg import stats_legend
from mylib.util.data import approx_num_bins


def plot_sig_mis(data, var, title, xlabel, xlim=(None, None)):
    """
    Plot the signal distribution and the misconstructed distribution
    on the same plot.
    """
    sig = data[data["isSignal"]==1].loc["det"][var]
    mis = data[data["isSignal"]==0].loc["det"][var]
    
    if xlim != (None, None):
        sig = sig[(sig > xlim[0]) & (sig < xlim[1])]
        mis = mis[(mis > xlim[0]) & (mis < xlim[1])]
    
    leg_sig = stats_legend(sig, "Detector: Signal")
    leg_mis = stats_legend(mis, "Detector: Misrecon.", show_mean=False, show_rms=False)

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
        mis,
        label=leg_mis,
        bins=approx_num_bins(mis),
        color="blue",
        histtype="step",
        linewidth=1,
    )

    ax.set_xlim(xlim)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    return fig, ax