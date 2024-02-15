
"""Efficiency plotting."""


import matplotlib.pyplot as plt

from mylib.util.data import (
    count_events, 
)
from mylib.calc.eff import (
    calc_eff, 
)
from mylib.plot.core.looks.lim import set_x_lims


def make_legend(num_gen, num_det):
    """Make the plot's legend."""

    legend = r"\textbf{Efficiency}" + f"\nDetector (signal): {num_det}\nGenerator: {num_gen}"
    return legend


def plot_eff(
    data_gen,
    data_det,
    num_points,
    title,
    xlabel,
    ylim=(0, 0.5),
    **kwargs,
):
    """Plot the efficiency."""

    eff, bin_mids, err = calc_eff(data_gen, data_det, num_points)

    fig, ax = plt.subplots()

    num_gen = count_events(data_gen)
    num_det = count_events(data_det)
    legend = make_legend(num_gen, num_det)

    ax.scatter(
        bin_mids, 
        eff,
        label=legend,
        color="red",
        alpha=1,
        **kwargs,
    )
    ax.errorbar(
        bin_mids,
        eff,
        yerr=err,
        fmt="none",
        capsize=5,
        color="black",
        alpha=0.5,
        **kwargs,
    )

    ax.legend()
    set_x_lims(ax, data_gen, data_det)
    ax.set_ymargin(0.25)
    ax.set_ylim(*ylim)
    ax.set_ylabel(r"$\varepsilon$", rotation=0, labelpad=20)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    return fig, ax


