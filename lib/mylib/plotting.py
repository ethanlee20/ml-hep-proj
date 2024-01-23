import os.path
import pathlib as pl
import itertools

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import eff_and_res
import preprocess as pre
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
    q_squared_region,
    num_points,
    title,
    xlabel,
    out_dir_path,
    **kwargs,
):

    efficiency, bin_middles, errors = eff_and_res.calculate_efficiency(
        data, variable, num_points, q_squared_region
    )

    fig, ax = plt.subplots()

    ax.scatter(
        bin_middles,
        efficiency,
        label=f"Detector (signal): {len(data.loc['det'])}\nGenerator: {len(data.loc['gen'])}",
        color="red",
        **kwargs,
    )
    ax.errorbar(
        bin_middles,
        efficiency,
        yerr=errors,
        fmt="none",
        capsize=5,
        color="black",
        **kwargs,
    )

    if variable=="chi":
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

    out_file_name = f"q2{q_squared_region}_eff_{variable}.png" 
    plt.savefig(out_dir_path.joinpath(out_file_name), bbox_inches="tight")
    plt.clf()


def plot_gen_det_compare(
    data,
    variable,
    q_squared_region, 
    title,
    xlabel,
    out_dir_path,
):

    data_gen = pre.preprocess(data, variable=variable, q_squared_region=q_squared_region, reconstruction_level="gen")
    data_det = pre.preprocess(data, variable=variable, q_squared_region=q_squared_region, reconstruction_level="det", signal_only=True)
    
    def approx_num_bins(data): 
        return round(np.sqrt(len(data)))

    num_bins = approx_num_bins(data_det)

    fig, ax = plt.subplots()
    ax.hist(
        data_gen,
        label=generate_stats_label(
            data_gen, 
            "Generator"
        ),    
        bins=num_bins,
        color="purple",
        histtype="step",
        linestyle="-",
    )

    ax.hist(
        data_det,
        label=generate_stats_label(
            data_det,
            "Detector (signal)"
        ),    
        bins=num_bins,
        color="blue",
        histtype="step",
    )

    if variable == "chi":
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

    file_name = f'q2{q_squared_region}_comp_{variable}.png'
    plt.savefig(out_dir_path.joinpath(file_name), bbox_inches='tight') 
    plt.clf()


def plot_resolution(
    data,
    variable,
    q_squared_region,
    title,
    xlabel, 
    out_dir_path,
):

    resolution = eff_and_res.calculate_resolution(
        data,
        variable,
        q_squared_region,
    )
    
    fig, ax = plt.subplots()
    
    ax.hist(
        resolution,
        label=generate_stats_label(resolution, "Signal Events"),
        bins=round(np.sqrt(len(resolution))),
        color="red",
        histtype="step",
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    out_file_name = f"q2{q_squared_region}_res_{variable}.png"
    plt.savefig(out_dir_path.joinpath(out_file_name), bbox_inches='tight')
    plt.clf()
    

def plot_candidate_multiplicity(data, out_dir_path):
    data_det = pre.preprocess(data, reconstruction_level="det")
    data_gen = pre.preprocess(data, reconstruction_level="gen")
        
    plt.hist(
        data_det["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=f"Detector (after cuts): {len(data.loc['det'])}", 
        color="red", 
        fill=False
    )

    plt.hist(
        data_gen["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=f"Generator: {len(data.loc['gen'])}", 
        color="blue", 
        fill=False
    )
    
    plt.title("Candidate Multiplicity")
    plt.xlabel("Candidates per Event")
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.legend()
    plt.savefig(out_dir_path.joinpath(f"cand_mult.png"), bbox_inches="tight")
    plt.clf()


def generate_plot_info(
    variables,
    xlabels,
    titles,
    q_squared_regions,
):

    info = [ (variable, xlabel, title, q_squared_region) 
        for (variable, xlabel, title), q_squared_region 
        in itertools.product(
            zip(variables, xlabels, titles), 
            q_squared_regions
        )
    ]     
    return info


def plot(
    plots, 
    data,
    out_dir_path
):
    """
    Plot given plot types.
    
    Possible plot types include: efficiency, resolution, generics, candidate multiplicity.
    
    Note: Assumes data contains generator and detector events
    as well as all regions of q squared.
    """
    if "efficiency" in plots:
        info = generate_plot_info(
            variables = ["costheta_K", "costheta_mu", "chi"],
            xlabels = [r"$\cos\theta_K$", r"$\cos\theta_\mu$", r"$\chi$"],
            titles = [r"Efficiency of $\cos\theta_K$", r"Efficiency of $\cos\theta_\mu$", r"Efficiency of $\chi$"],
            q_squared_regions = ["all", "med"],
        )
        
        [ 
            plot_efficiency(
                data=data,
                variable=variable,
                q_squared_region=q_squared_region,
                num_points=20,
                title=title,
                xlabel=xlabel,
                out_dir_path=out_dir_path,
            )
            for variable, xlabel, title, q_squared_region in info
        ]
    
    if "resolution" in plots:
        info = generate_plot_info(
            variables = ["costheta_K", "costheta_mu", "chi"],
            xlabels = [r"$\cos\theta_K - \cos\theta_K^{MC}$", r"$\cos\theta_\mu - \cos\theta_\mu^{MC}$", r"$\chi - \chi^{MC}$"],
            titles = [r"Resolution of $\cos\theta_K$", r"Resolution of $\cos\theta_\mu$", r"Resolution of $\chi$"],
            q_squared_regions = ["all", "med"],
        )
                
        [ 
            plot_resolution(
                data=data,
                variable=variable,
                q_squared_region=q_squared_region,
                title=title,
                xlabel=xlabel,
                out_dir_path=out_dir_path,
            )
            for variable, xlabel, title, q_squared_region in info
        ]

    if "candidate multiplicity" in plots:
        plot_candidate_multiplicity(data, out_dir_path)
    
    if "generics" in plots:

        info = generate_plot_info(
            variables = ["costheta_K", "costheta_mu", "chi", "q_squared"],
            xlabels = [r"", r"", r"", r"GeV$^2$"],
            titles = [r"$\cos\theta_K$", r"$\cos\theta_\mu$", r"$\chi$", r"$q^2$"],
            q_squared_regions = ["all", "med"],
        )

        for variable, xlabel, title, q_squared_region in info:
            plot_gen_det_compare(
                data,
                variable=variable,
                q_squared_region=q_squared_region, 
                title=title,
                xlabel=xlabel,
                out_dir_path=out_dir_path
            )    


