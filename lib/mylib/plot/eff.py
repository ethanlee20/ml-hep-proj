
"""Efficiency plotting."""


import matplotlib.pyplot as plt

from mylib.util.data import (
    count_events, 
)
from mylib.calc.eff import (
    calc_eff, 
)
from mylib.plot.core.looks.lim import set_x_lims

from mylib.util.data import section
from mylib.plot.core.util.save import save
from mylib.util.iter import over_q_squared_splits




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
    
    def make_legend(num_gen, num_det):
        """Make the plot's legend."""
        legend = r"\textbf{Efficiency}" + f"\nDetector (signal): {num_det}\nGenerator: {num_gen}"
        return legend


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
    ax.set_ylim(ylim)
    ax.set_ylabel(r"$\varepsilon$", rotation=0, labelpad=20)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    return fig, ax


def plot_gen_eff(
    data_gen,
    data_gen_cut,
    num_points,
    title,
    xlabel,
    ylim=(0, 1),
    **kwargs,
):
    """Plot recreated efficiency using cuts on generator level data."""
  
    def make_legend(num_gen, num_gen_cut):
        """Make the plot's legend."""
        legend = r"\textbf{Generator Efficiency}" + f"\nCut Generator: {num_gen_cut}\nGenerator: {num_gen}"
        return legend

    eff, bin_mids, err = calc_eff(data_gen, data_gen_cut, num_points)

    fig, ax = plt.subplots()

    num_gen = count_events(data_gen)
    num_gen_cut = count_events(data_gen_cut)
    legend = make_legend(num_gen, num_gen_cut)

    ax.scatter(
        bin_mids, 
        eff,
        label=legend,
        color="red",
        alpha=0.5,
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
    set_x_lims(ax, data_gen, data_gen_cut)
    ax.set_ymargin(0.25)
    ax.set_ylim(*ylim)
    ax.set_ylabel(r"$\varepsilon_\text{Gen}$", rotation=0, labelpad=20)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    return fig, ax


@over_q_squared_splits
def eff_cos_theta_k(data, out_dir, q_squared_split):

    data = section(data, only_sig=True, var="costheta_K", q_squared_split=q_squared_split)
    data_gen = data.loc["gen"]
    data_det = data.loc["det"]

    fig, ax = plot_eff(
        data_gen,
        data_det,
        num_points=100,
        title=r"Efficiency of $\cos\theta_K$",
        xlabel=r"$\cos\theta_K$",
    )
    save("eff_costheta_k", q_squared_split, out_dir)


@over_q_squared_splits
def eff_cos_theta_e(data, out_dir, q_squared_split):

    data = section(data, only_sig=True, var="costheta_e", q_squared_split=q_squared_split)
    data_gen = data.loc["gen"]
    data_det = data.loc["det"]

    fig, ax = plot_eff(
        data_gen,
        data_det,
        num_points=100,
        title=r"Efficiency of $\cos\theta_e$",
        xlabel=r"$\cos\theta_e$",
    )
    save("eff_costheta_e", q_squared_split, out_dir)


@over_q_squared_splits
def eff_chi(data, out_dir, q_squared_split):

    data = section(data, only_sig=True, var="chi", q_squared_split=q_squared_split)
    data_gen = data.loc["gen"]
    data_det = data.loc["det"]
    
    fig, ax = plot_eff(
        data_gen,
        data_det,
        num_points=100,
        title=r"Efficiency of $\chi$",
        xlabel=r"$\chi$",
    )
    save("eff_chi", q_squared_split, out_dir)
