

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



"""Efficiency plotting."""

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


