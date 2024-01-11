import os.path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import eff_and_res
import util


def setup_mpl_params_save():
    # plt.style.use("belle2")
    mpl.rcParams["figure.figsize"] = (8, 5)
    mpl.rcParams["figure.dpi"] = 200
    mpl.rcParams["axes.titlesize"] = 32
    mpl.rcParams["axes.labelsize"] = 28
    mpl.rcParams["xtick.labelsize"] = 20
    mpl.rcParams["ytick.labelsize"] = 20
    mpl.rcParams["text.usetex"] = True
    mpl.rcParams[
        "text.latex.preamble"
    ] = r"\usepackage{physics}"
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.serif"] = ["Computer Modern"]


def setup_mpl_params_view():
    # plt.style.use("belle2")
    mpl.rcParams["figure.figsize"] = (6, 4)
    mpl.rcParams["figure.dpi"] = 150
    mpl.rcParams["axes.titlesize"] = 32
    mpl.rcParams["axes.labelsize"] = 28
    mpl.rcParams["xtick.labelsize"] = 20
    mpl.rcParams["ytick.labelsize"] = 20
    mpl.rcParams["text.usetex"] = True
    mpl.rcParams[
        "text.latex.preamble"
    ] = r"\usepackage{physics}"
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.serif"] = ["Computer Modern"]


def generate_stats_label(
    x,
    descrp="",
    show_mean=True,
    show_count=True,
    show_rms=True,
):
    def stats(x):
        mean = np.mean(x)
        count = x.count()
        rms = np.std(x)
        collection = {
            "mean": mean,
            "count": count,
            "rms": rms,
        }
        return collection

    stats = stats(x)

    stats_label = ""
    if descrp != "":
        stats_label += r"\textbf{" + f"{descrp}" + "}"
    if show_mean:
        stats_label += f"\nMean: {round(stats['mean'], 2)}"
    if show_count:
        stats_label += f"\nCount: {stats['count']}"
    if show_rms:
        stats_label += f"\nRMS: {round(stats['rms'], 2)}"

    return stats_label


def plot_signal_and_misrecon(
    var, df, q_squared_slice, reconstruction_level, title, xlabel, out_dir_path, radians=False, **kwargs
):
    df = df.loc[reconstruction_level]

    if q_squared_slice=="med":
        df = df[(df["q_squared"] > 1) & (df["q_squared"] < 6)]
    elif q_squared_slice=="all":
        df = df

    signal = df[df["isSignal"] == 1][var]
    misrecon = df[df["isSignal"] == 0][var]

    signal_label = generate_stats_label(
        signal, descrp="Signal"
    )
    misrecon_label = generate_stats_label(
        misrecon,
        descrp="Misrecon.",
        show_mean=False,
        show_rms=False,
    )

    fig, ax = plt.subplots()

    def sqrt_of_count(x):
        return np.sqrt(len(x))

    bins = round(sqrt_of_count(signal))

    ax.hist(
        signal,
        label=signal_label,
        bins=bins,
        alpha=0.6,
        color="red",
        histtype="stepfilled",
        **kwargs,
    )

    ax.hist(
        misrecon,
        label=misrecon_label,
        bins=bins,
        color="blue",
        histtype="step",
        linewidth=1,
        **kwargs,
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    if radians:
        plt.xticks(
            [0, np.pi / 2, np.pi, (3 / 2) * np.pi, 2 * np.pi],
            [
                r"$0$",
                r"$\frac{\pi}{2}$",
                r"$\pi$",
                r"$\frac{3\pi}{2}$",
                r"$2\pi$",
            ],
        )
            
    file_name = f'q2{q_squared_slice}_{reconstruction_level}_{var}.png'
    plt.savefig(out_dir_path.joinpath(file_name), bbox_inches='tight') 
    plt.clf()
    

def plot_image(
    path_image_pickle_file,
    name_column_costheta_mu_bin,
    name_column_costheta_k_bin,
    name_column_chi_bin,
    name_column_q_squared,
    num_events,
):
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


def plot_efficiency(
    data_recon,
    data_gen,
    variable,
    num_data_points,
    title,
    xlabel,
    **kwargs,
):
    data_min = np.min(
        [
            data_recon[variable].min(),
            data_gen[variable].min(),
        ]
    )
    data_max = np.max(
        [
            data_recon[variable].max(),
            data_gen[variable].max(),
        ]
    )
    bin_edges = eff_and_res.generate_bin_edges(
        start=data_min,
        stop=data_max,
        num_of_bins=num_data_points,
    )

    efficiency = eff_and_res.calculate_efficiency(
        data_recon, data_gen, variable, bin_edges
    )
    efficiency_errorbars = (
        eff_and_res.calculate_efficiency_errorbars(
            data_recon, data_gen, variable, bin_edges
        )
    )

    bin_middles = eff_and_res.find_bin_middles(bin_edges)

    fig, ax = plt.subplots()
    ax.scatter(
        bin_middles,
        efficiency,
        label=f"Entries (Generator): {len(data_gen)}\nEntries (Reconstructed): {len(data_recon)}",
        color="red",
        **kwargs,
    )
    ax.errorbar(
        bin_middles,
        efficiency,
        yerr=efficiency_errorbars,
        fmt="none",
        capsize=5,
        color="black",
        **kwargs,
    )
    plt.ylim(bottom=0)
    ax.legend()
    ax.set_xlim(data_min - 0.05, data_max + 0.05)
    ax.set_ylabel(r"$\varepsilon$", rotation=0, labelpad=20)
    ax.set_xlabel(xlabel)
    ax.set_title(title)


def plot_gen_recon_compare(
    data_gen,
    data_recon,
    variable,
    title,
    xlabel,
    radians=False,
):
    def sqrt_of_count(data):
        return np.sqrt(len(data))

    num_bins = round(sqrt_of_count(data_recon))

    fig, ax = plt.subplots()
    ax.hist(
        data_gen[variable],
        label=f"Generator (Entries: {len(data_gen[variable])})",
        bins=num_bins,
        color="purple",
        histtype="step",
        linestyle="-",
    )

    ax.hist(
        data_recon[variable],
        label=f"Reconstructed (Entries: {len(data_recon[variable])})",
        bins=num_bins,
        color="blue",
        histtype="step",
    )

    if radians:
        plt.xticks(
            [
                0,
                np.pi / 2,
                np.pi,
                (3 / 2) * np.pi,
                2 * np.pi,
            ],
            [
                r"$0$",
                r"$\frac{\pi}{2}$",
                r"$\pi$",
                r"$\frac{3\pi}{2}$",
                r"$2\pi$",
            ],
        )
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)


def plot_resolution(
    var, mc_truth_var, data, title, xlabel, periodic=False
):
    signal_data = data[data["isSignal"] == 1]

    resolution = (
       signal_data[var] - signal_data[mc_truth_var] 
    )

    if periodic:
        resolution = resolution.where(
            resolution < np.pi, resolution - 2 * np.pi
        )
        resolution = resolution.where(
            resolution > -np.pi, resolution + 2 * np.pi
        )

    fig, ax = plt.subplots()

    ax.hist(
        resolution,
        label=f"Signal Events: {len(signal_data)}",
        bins=round(np.sqrt(len(signal_data))),
        color="red",
        histtype="step",
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
