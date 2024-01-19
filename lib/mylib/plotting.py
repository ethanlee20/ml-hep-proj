import os.path
import pathlib as pl

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
    var, 
    df, 
    q_squared_slice, 
    reconstruction_level, 
    title, 
    xlabel, 
    out_dir_path, 
    radians=False, 
    **kwargs
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
    data,
    variable,
    q_squared_split,
    num_data_points,
    title,
    xlabel,
    out_dir_path,
    radians=False,
    **kwargs,
):

    if q_squared_split == "med":
        data = data[(data['q_squared']>1)&(data['q_squared']<6)]
    elif q_squared_split == "all":
        data = data

    data = data[data["isSignal"]==1]
    
    data_gen = data.loc['gen']
    data_det = data.loc['det']
        
    bin_edges = eff_and_res.generate_bin_edges(
        start=data[variable].min(),
        stop=data[variable].max(),
        num_of_bins=num_data_points,
    )

    bin_middles = eff_and_res.find_bin_middles(bin_edges)

    efficiency = eff_and_res.calculate_efficiency(
        data_det, data_gen, variable, bin_edges
    )
    
    efficiency_errorbars = (
        eff_and_res.calculate_efficiency_errorbars(
            data_det, data_gen, variable, bin_edges
        )
    )


    fig, ax = plt.subplots()
    ax.scatter(
        bin_middles,
        efficiency,
        label=f"Detector: {len(data_det)}\nGenerator: {len(data_gen)}",
        color="red",
        **kwargs,
    )
    ax.errorbar(
        bin_middles,
        e--fficiency,
        yerr=efficiency_errorbars,
        fmt="none",
        capsize=5,
        color="black",
        **kwargs,
    )

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

    ax.legend()
    ax.set_xlim(data[variable].min() - 0.05, data[variable].max() + 0.05)
    ax.set_ymargin(0.25)
    ax.set_ylim(bottom=0, top=0.5)
    ax.set_ylabel(r"$\varepsilon$", rotation=0, labelpad=20)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    out_file_name = f"q2{q_squared_split}_eff_{variable}.png" 
    plt.savefig(out_dir_path.joinpath(out_file_name), bbox_inches="tight")
    plt.clf()


def plot_gen_det_compare(
    variable,
    data,
    q_squared_split, 
    title,
    xlabel,
    out_dir_path,
    radians=False,
):

    data_gen = data.loc['gen']
    data_det = data.loc['det']
    
    if q_squared_split == "med":
        data_gen = data_gen[(data_gen['q_squared']>1)&(data_gen['q_squared']<6)]
        data_det = data_det[(data_det['q_squared']>1)&(data_det['q_squared']<6)]

    elif q_squared_split == "all":
        data_gen = data_gen
        data_det = data_det

    def approx_num_bins(data): 
        return round(np.sqrt(len(data)))

    num_bins = approx_num_bins(data_det)

    fig, ax = plt.subplots()
    ax.hist(
        data_gen[variable],
        label=generate_stats_label(
            data_gen[variable], 
            "Generator"
        ),    
        bins=num_bins,
        color="purple",
        histtype="step",
        linestyle="-",
    )

    ax.hist(
        data_det[variable],
        label=generate_stats_label(
            data_det[variable],
            "Detector (signal)"
        ),    
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

    file_name = f'q2{q_squared_split}_comp_{variable}.png'
    plt.savefig(out_dir_path.joinpath(file_name), bbox_inches='tight') 

    plt.clf()


def plot_resolution(
    vars, 
    q_squared_splits,
    data,
    out_dir_path,
):

    titles = dict(
        costheta_mu=r"Resolution of $\cos\theta_\mu$", 
        costheta_K=r"Resolution of $\cos\theta_K$", 
        chi=r"Resolution of $\chi$"
    )

    xlabels = dict(
        costheta_mu=r"$\cos\theta_\mu - \cos\theta_\mu^\text{MC}$", 
        costheta_K=r"$\cos\theta_K - \cos\theta_K^\text{MC}$", 
        chi=r"$\chi - \chi^\text{MC}$"
    )

    for resolution, calc_info in eff_and_res.calculate_resolutions(
        vars, q_squared_splits, data.loc["det"]
    ): 
        fig, ax = plt.subplots()
        
        ax.hist(
            resolution,
            label=generate_stats_label(resolution, "Signal Events"),
            bins=round(np.sqrt(len(resolution))),
            color="red",
            histtype="step",
        )

        ax.legend()
        ax.set_title(titles[calc_info["var"]])
        ax.set_xlabel(xlabels[calc_info["var"]])

        out_file_name = f"q2{calc_info['split']}_res_{calc_info['var']}.png"
        plt.savefig(out_dir_path.joinpath(out_file_name), bbox_inches='tight')


def plot_candidate_multiplicity(data, out_dir_path):
    datas = (data.loc['gen'], data.loc['det'])
    labels = (
        f"Generator: {len(data.loc['gen'])}",
        f"Detector (after cuts): {len(data.loc['det'])}"
    )
    file_ids = ('gen', 'det')
    
    for data, label, id  in zip(datas, labels, file_ids):
        plt.hist(
            data["__event__"].value_counts().values, 
            bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
            label=label, 
            color="red", 
            fill=True
        )
        plt.title("Candidate Multiplicity")
        plt.xlabel("Candidates per Event")
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        plt.legend()
        plt.savefig(out_dir_path.joinpath(f"cand_mult_{id}.png"), bbox_inches="tight")
        plt.clf()

