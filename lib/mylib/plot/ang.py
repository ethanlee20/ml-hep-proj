
from mylib.plot.core.util.save import save
from mylib.util.iter import over_q_squared_splits

from mylib.plot.hist_1d.gen_det import plot_gen_det


@over_q_squared_splits
def hist_chi(data, out_dir, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="chi",
        q_squared_split=q_squared_split,
        title=r"$\chi$",
        xlabel=None,
    )
    save("chi", q_squared_split, out_dir)


@over_q_squared_splits
def hist_costheta_e(data, out_dir, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="costheta_e",
        q_squared_split=q_squared_split,
        title=r"$\cos\theta_e$",
        xlabel=None,
    )
    save("hist_costheta_e", q_squared_split, out_dir)


@over_q_squared_splits
def hist_costheta_mu(data, out_dir, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="costheta_mu",
        q_squared_split=q_squared_split,
        title=r"$\cos\theta_\mu$",
        xlabel=None,
    )
    save("hist_costheta_mu", q_squared_split, out_dir)


@over_q_squared_splits
def hist_costheta_K(data, out_dir, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="costheta_K",
        q_squared_split=q_squared_split,
        title=r"$\cos\theta_K$",
        xlabel=None,
    )
    save("hist_costheta_K", q_squared_split, out_dir)


@over_q_squared_splits
def hist_q_squared(data, out_dir, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="q_squared",
        q_squared_split=q_squared_split,
        title=r"$q^2$",
        xlabel="[GeV$^2$]",
    )
    save("hist_q_squared", q_squared_split, out_dir)