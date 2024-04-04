from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from mylib.util import (
    approx_num_bins, 
    bin_data, 
    count_events, 
    find_bin_counts, 
    find_bin_middles, 
    make_bin_edges, 
    min_max_over_arrays, 
    noise_, sig_,
    section, 
)


def setup_mpl_params_save():
    """Setup plotting parameters."""
    mpl.rcParams["figure.figsize"] = (8, 5)
    mpl.rcParams["figure.dpi"] = 200
    mpl.rcParams["axes.titlesize"] = 28
    mpl.rcParams["figure.titlesize"] = 32
    mpl.rcParams["axes.labelsize"] = 26
    mpl.rcParams["figure.labelsize"] = 30
    mpl.rcParams["xtick.labelsize"] = 20
    mpl.rcParams["ytick.labelsize"] = 20
    mpl.rcParams["text.usetex"] = True
    mpl.rcParams[
        "text.latex.preamble"
    ] = r"\usepackage{physics}"
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.serif"] = ["Computer Modern"]


def save_plot(plot_name, q_squared_split, out_dir):
    """Save plot."""

    def _plot_file_name(plot_name, q_squared_split):
        return f"q2{q_squared_split}_{plot_name}.png"

    def _save_fig_and_clear(file_name, out_dir):
        plt.savefig(out_dir.joinpath(file_name), bbox_inches="tight")
        plt.close()

    file_name = _plot_file_name(plot_name, q_squared_split)
    _save_fig_and_clear(file_name, out_dir)


def set_x_lims(ax, data_gen, data_det):
    """Set the plot's x limits to contain all the data."""

    min, max = min_max_over_arrays([data_gen, data_det])
    ax.set_xlim(min - 0.05, max + 0.05)


def ticks_in_radians(axis, kind):
    """Change axis ticks to units of pi."""

    zero_to_two_pi = {
        'nums':[0, np.pi/2, np.pi, (3/2)*np.pi, 2*np.pi],
        'syms':[r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"]
    }         

    zero_to_pi = {
        'nums':[0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi],
        'syms': [r"$0$", r"$\frac{\pi}{4}$", r"$\frac{\pi}{2}$", r"$\frac{3\pi}{4}$", r"$\pi$"]
    }

    if axis == "x":
        ticks = plt.xticks
    elif axis == "y":
        ticks = plt.yticks
        
    if kind == "0 to 2pi":
        ticks(zero_to_two_pi.nums, zero_to_two_pi.syms)
    elif kind == "0 to pi":
        ticks(zero_to_pi.nums, zero_to_pi.syms) 
    else: raise ValueError(f"Unrecognized kind: {kind}")


def stats_legend(
    dat_ser,
    descrp="",
    show_mean=True,
    show_count=True,
    show_rms=True,
):
    """Make a legend label similar to the roots stats box."""
    
    def calculate_stats(ar):
        mean = np.mean(ar)
        count = count_events(ar)
        rms = np.std(ar)
        stats = {
            "mean": mean,
            "count": count,
            "rms": rms,
        }
        return stats
    
    stats = calculate_stats(dat_ser)

    leg = ""
    if descrp != "":
        leg += r"\textbf{" + f"{descrp}" + "}"
    if show_mean:
        leg += f"\nMean: {stats['mean']:.2G}"
    if show_count:
        leg += f"\nCount: {stats['count']}"
    if show_rms:
        leg += f"\nRMS: {stats['rms']:.2G}"

    return leg


def plot_gen_det(
    data,
    var,
    q_squared_split, 
    title,
    xlabel,
    xlim=(None, None)
):
    """Plot the generator level distribution alongside the detector level distribution."""

    data = section(data, only_sig=True, var=var, q_squared_split=q_squared_split)

    if xlim not in {(None, None), None}:
        data = data[(data > xlim[0]) & (data < xlim[1])]

    legends = {
        "gen":stats_legend(data.loc["gen"], "Generator"), 
        "det":stats_legend(data.loc["det"], "Detector (signal)")
    }

    fig, ax = plt.subplots()

    ax.hist(
        data.loc["gen"],
        label=legends["gen"],    
        bins=approx_num_bins(data.loc["gen"]),
        color="purple",
        histtype="step",
        linestyle="-",
    )

    ax.hist(
        data.loc["det"],
        label=legends["det"],    
        bins=approx_num_bins(data.loc["det"]),
        color="blue",
        histtype="step",
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    return fig, ax


def plot_sig_noise(data, var, q_squared_split, noise_type, title, xlabel, out_dir, xlim=(None, None), scale='linear', extra_name=""):
    """
    Plot the signal distribution and the noise distribution
    on the same plot.
    """
    
    sig = section(data.loc["det"], sig_noise='sig', var=var, q_squared_split=q_squared_split)
    noise = section(data.loc["det"], sig_noise='noise', var=var, q_squared_split=q_squared_split)
    
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

    ax.yscale(scale)
    # ax.set_xlim(xlim)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    save_plot(
        plot_name=f"sig_noise_{var}_{extra_name}",
        q_squared_split=q_squared_split,
        out_dir=out_dir
    )


def plot_image(
    path_image_pickle_file,
    name_column_costheta_mu_bin,
    name_column_costheta_k_bin,
    name_column_chi_bin,
    name_column_q_squared,
    num_events,
):
    """Plot one of the images (i.e. angular distributions)."""

    image = pd.read_pickle(path_image_pickle_file)
    with mpl.rc_context():
        mpl.rcParams["figure.figsize"] = (6, 5)
        mpl.rcParams["axes.titlesize"] = 28
        mpl.rcParams["axes.labelsize"] = 24

        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        sc = ax.scatter(
            image[name_column_costheta_mu_bin],
            image[name_column_costheta_k_bin],
            image[name_column_chi_bin],
            c=image[name_column_q_squared],
            cmap="magma",
        )
        ax.set_title(r"Average $q^2$ per Angular Bin")
        ax.set_xlabel(r"$\cos\theta_\mu$ Bin", labelpad=10)
        ax.set_ylabel(r"$\cos\theta_K$ Bin", labelpad=10)
        ax.set_zlabel(r"$\chi$ Bin", labelpad=10)
        ax.tick_params(pad=1)
        ax.annotate(
            f"Num. Events: {num_events}",
            (190, 250),
            xycoords="axes points",
            fontsize="xx-large",
        )
        fig.colorbar(
            sc,
            ax=ax,
            pad=0.025,
            shrink=0.6,
            location="left",
        )


def calc_eff(data_gen, data_det, num_points):
    """
    Calculate the efficiency per bin.
    
    The efficiency of bin i is defined as the number of
    detector entries in i divided by the number of generator
    entries in i.
    
    The errorbar for bin i is calculated as the squareroot of the
    number of detector entries in i divided by the number of
    generator entries in i.
    """
    min, max = min_max_over_arrays([data_gen, data_det])
    bin_edges = make_bin_edges(start=min, stop=max, num_bins=num_points)
    bin_mids = find_bin_middles(bin_edges)

    binned_gen = bin_data(data_gen, bin_edges)
    binned_det = bin_data(data_det, bin_edges)

    bin_count_gen = find_bin_counts(binned_gen)
    bin_count_det = find_bin_counts(binned_det)
    
    eff = (bin_count_det / bin_count_gen).values
    err = (np.sqrt(bin_count_det) / bin_count_gen).values
    
    return eff, bin_mids, err


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
    """Attempt to recreate efficiency plot using cuts on generator level data."""
  
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


def calculate_resolution(data, variable, q_squared_split):
    """
    Calculate the resolution.
    
    The resolution of a variable is defined as the 
    reconstructed value minus the MC truth value.
    """
    data_calc = section(data, sig_noise='sig', var=variable, q_squared_split=q_squared_split).loc["det"]
    data_mc = section(data, sig_noise='sig', var=variable+'_mc', q_squared_split=q_squared_split).loc["det"]
    
    resolution = data_calc - data_mc

    if variable != "chi":
        return resolution

    def apply_periodicity(resolution):
        resolution = resolution.where(
                resolution < np.pi, resolution - 2 * np.pi
        )
        resolution = resolution.where(
            resolution > -np.pi, resolution + 2 * np.pi
        )
        return resolution

    return apply_periodicity(resolution)


def plot_resolution(
    data,
    variable,
    q_squared_split,
    title,
    xlabel, 
    out_dir_path,
    xlim=(None, None),
):
    """Plot the resolution."""

    resolution = calculate_resolution(
        data,
        variable,
        q_squared_split,
    )

    if xlim not in {(None, None), None}:
        resolution = resolution[(resolution > xlim[0]) & (resolution < xlim[1])]

    fig, ax = plt.subplots()
    
    ax.hist(
        resolution,
        label=stats_legend(resolution, "Signal Events"),
        bins=approx_num_bins(resolution),
        color="red",
        histtype="step",
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    file_name = f"q2{q_squared_split}_res_{variable}.png"

    save_plot(
        plot_name=f'res_{variable}',
        q_squared_split=q_squared_split,
        out_dir=out_dir_path
    )


def plot_candidate_multiplicity(data, out_dir_path, ell):
    """Plot a histogram of the candidate multiplicity."""

    sig = sig_(data).loc["det"]
    noise = noise_(data).loc["det"]

    plt.hist(
        sig["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=stats_legend(sig["__event__"], descrp="Signal (after cuts)", show_mean=False, show_rms=False),
        color="red", 
        alpha=0.6,
        histtype="stepfilled"
    )
    
    plt.hist(
        noise["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=stats_legend(noise["__event__"], descrp="Misrecon. (after cuts)", show_mean=False, show_rms=False),
        color="blue", 
        histtype="step"
    )
    if ell == "mu":
        plt.title(r"Candidate Multiplicity ($\ell = \mu$)")
    elif ell == "e":
        plt.title(r"Candidate Multiplicity ($\ell = e$)")
    else: raise Exception()
    plt.xlabel("Candidates per Event")
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.legend()

    save_plot(
        plot_name="cand_mult",
        q_squared_split="all",
        out_dir=out_dir_path
    )


def plot_hist_2d_side_by_side(
    xs,
    ys,
    num_bins,
    cmap
):
    """Plot two 2d-histograms side-by-side."""

    def subplots_side_by_side():
        fig, axs = plt.subplots(ncols=2, layout="constrained", sharey=True)
        return fig, axs

    def multi_hist_norm(hists):
        _, max_counts = min_max_over_arrays(hists)
        norm = plt.Normalize(0, max_counts)    
        return norm

    def calc_multi_hist_2d(xs: list, ys: list, num_bins: int):
        assert len(xs) == len(ys)
        xmin, xmax = min_max_over_arrays(xs)
        ymin, ymax = min_max_over_arrays(ys)
        interval = ((xmin, xmax), (ymin, ymax))
        hists = [np.histogram2d(x, y, num_bins, interval) for x, y in zip(xs, ys)]
        return hists
        
    def add_hist_2d(ax, hist_2d, norm, cmap):
        h = hist_2d[0]
        x_edges = hist_2d[1]
        y_edges = hist_2d[2]
        ax.pcolormesh(x_edges, y_edges, h.T, norm=norm, cmap=cmap)

    assert((len(xs) == 2) & (len(ys) == 2))

    hists = calc_multi_hist_2d(xs, ys, num_bins)
    hs = [hist[0] for hist in hists]
    norm = multi_hist_norm(hs)

    fig, axs = subplots_side_by_side()
    for hist, ax in zip(hists, axs):
        add_hist_2d(ax, hist, norm, cmap)

    return fig, axs, norm


def add_color_bar(axs, norm, cmap):
    """Add a colorbar scaled to multiple axes."""

    def scalar_mappable(norm, cmap):
        return mpl.cm.ScalarMappable(norm, cmap=cmap)
    
    sm = scalar_mappable(norm, cmap)
    plt.colorbar(sm, ax=axs, aspect=30)


def hist2d_sig_noise(data, xvar, yvar, out_dir, n_bins, xlabel, ylabel, save_name, cmap="magma"):
    """Plot 2d-histogram of signal next to 2d-histogram of noise."""

    sig = sig_(data).loc["det"]
    noise = noise_(data).loc["det"]

    fig, axs, norm = plot_hist_2d_side_by_side(
        xs=[
            sig[xvar],
            noise[xvar],
        ],
        ys=[
            sig[yvar],
            noise[yvar],
        ],
        num_bins=n_bins,
        cmap=cmap
    )

    add_color_bar(axs, norm, cmap=cmap)

    axs[0].set_title(r"Signal \small" + f"(count: {count_events(sig)})")
    axs[1].set_title(r"Bkg. and Misrecon. \small" + f"(count: {count_events(noise)})")
    fig.supxlabel(xlabel)
    axs[0].set_ylabel(ylabel)
    save_plot(save_name, q_squared_split="all", out_dir=out_dir)


def hist2d_sig(data, xvar, yvar, out_dir, n_bins, xrange, yrange, xlabel, ylabel, scale, save_name, cmap="magma"):
    """Plot 2d-histogram of signal."""

    sig = sig_(data).loc["det"]
    plt.hist2d(sig[xvar], sig[yvar], bins=n_bins, cmap=cmap, range=(xrange, yrange), norm=scale)
    plt.colorbar()
    plt.title(r"Signal \small" + f"(count: {count_events(sig)})")
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    save_plot(save_name, q_squared_split="all", out_dir=out_dir)

