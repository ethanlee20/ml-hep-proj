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


def save_fig_and_clear(out_dir_path, file_name):
    plt.savefig(out_dir_path.joinpath(file_name), bbox_inches="tight")
    plt.close()


def approx_num_bins(data_series):
    return round(np.sqrt(len(data_series)))


def x_axis_in_radians(kind):
    if kind == "0 to 2pi":
        plt.xticks(
            [
                0, 
                np.pi / 2, 
                np.pi, 
                (3 / 2) * np.pi, 
                2 * np.pi
            ],
            [
                r"$0$",
                r"$\frac{\pi}{2}$",
                r"$\pi$",
                r"$\frac{3\pi}{2}$",
                r"$2\pi$",
            ],
        )

    else: raise ValueError(f"Unrecognized kind: {type}")


def y_axis_in_radians(kind):
    if kind == "0 to 2pi":
        plt.yticks(
            [
                0, 
                np.pi / 2, 
                np.pi, 
                (3 / 2) * np.pi, 
                2 * np.pi
            ],
            [
                r"$0$",
                r"$\frac{\pi}{2}$",
                r"$\pi$",
                r"$\frac{3\pi}{2}$",
                r"$2\pi$",
            ],
        )
    elif kind == "0 to pi":
        plt.yticks(
            [
                0,
                np.pi / 4, 
                np.pi / 2,
                3 * np.pi / 4, 
                np.pi, 
            ],
            [
                r"$0$",
                r"$\frac{\pi}{4}$",
                r"$\frac{\pi}{2}$",
                r"$\frac{3\pi}{4}$",
                r"$\pi$",
            ],
        )

        

    else: raise ValueError(f"Unrecognized kind: {type}")


def generate_stats_label(
    data_series,
    descrp="",
    show_mean=True,
    show_count=True,
    show_rms=True,
):
    def stats(data_series):
        mean = np.mean(data_series)
        count = data_series.count()
        rms = np.std(data_series)
        collection = {
            "mean": mean,
            "count": count,
            "rms": rms,
        }
        return collection

    stats = stats(data_series)

    stats_label = ""
    if descrp != "":
        stats_label += r"\textbf{" + f"{descrp}" + "}"
    if show_mean:
        stats_label += f"\nMean: {stats['mean']:.2G}"
    if show_count:
        stats_label += f"\nCount: {stats['count']}"
    if show_rms:
        stats_label += f"\nRMS: {stats['rms']:.2G}"

    return stats_label


def plot_signal_and_misrecon(
    data,
    variable, 
    q_squared_region, 
    reconstruction_level, 
    title, 
    xlabel, 
    out_dir_path, 
    **kwargs
):
    data = pre.preprocess(
        data=data,
        variables=variable,
        q_squared_region=q_squared_region,
        reconstruction_level=reconstruction_level
    )

    signal = data[data["isSignal"] == 1]
    misrecon = data[data["isSignal"] == 0]

    signal_label = generate_stats_label(
        signal, 
        descrp="Signal",
    )
    misrecon_label = generate_stats_label(
        misrecon,
        descrp="Misrecon.",
        show_mean=False,
        show_rms=False,
    )

    bins = approx_num_bins(signal)

    fig, ax = plt.subplots()

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

    if variable == "chi":
        x_axis_in_radians(kind="0 to 2pi")
            
    file_name = f'q2{q_squared_region}_{reconstruction_level}_{variable}.png'

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name=file_name,
    )
    

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
    mc_truth_comp=False,
    **kwargs,
):

    efficiency, bin_middles, errors = eff_and_res.calculate_efficiency(
        data, variable, num_points, q_squared_region
    )

    num_det_events = len(
        pre.preprocess(
            data=data,
            q_squared_region=q_squared_region,
            reconstruction_level="det",
            signal_only=True,
        )
    )

    num_gen_events = len(
        pre.preprocess(
            data=data,
            q_squared_region=q_squared_region,
            reconstruction_level="gen",
        )
    )

    if mc_truth_comp:
        efficiency_mc, bin_middles_mc, errors_mc = eff_and_res.calculate_efficiency(
            data, variable, num_points, q_squared_region, mc=True
        )

    fig, ax = plt.subplots()

    ax.scatter(
        bin_middles, 
        efficiency,
        label=r"\textbf{Calculated}"+f"\nDetector (signal): {num_det_events}\nGenerator: {num_gen_events}",
        color="red",
        alpha=0.5,
        **kwargs,
    )
    ax.errorbar(
        bin_middles,
        efficiency,
        yerr=errors,
        fmt="none",
        capsize=5,
        color="black",
        alpha=0.5,
        **kwargs,
    )

    if mc_truth_comp:
        ax.scatter(
            bin_middles_mc,
            efficiency_mc,
            label=r"\textbf{MC Truth}",
            color="blue",
            alpha=0.5,
            **kwargs,
        )
        ax.errorbar(
            bin_middles_mc,
            efficiency_mc,
            yerr=errors_mc,
            fmt="none",
            capsize=5,
            color="orange",
            alpha=0.5,
            **kwargs,
        )

    if variable=="chi":
        x_axis_in_radians(kind="0 to 2pi")

    ax.legend()
    ax.set_xlim(data[variable].min() - 0.05, data[variable].max() + 0.05)
    ax.set_ymargin(0.25)
    ax.set_ylim(bottom=0, top=0.5)
    ax.set_ylabel(r"$\varepsilon$", rotation=0, labelpad=20)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    file_name = f"q2{q_squared_region}_eff_{variable}.png" 

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name=file_name,
    )


def plot_gen_det_compare(
    data,
    variable,
    q_squared_region, 
    title,
    xlabel,
    out_dir_path,
):

    data_gen = pre.preprocess(
        data, 
        variables=variable, 
        q_squared_region=q_squared_region, 
        reconstruction_level="gen"
    )
    data_det = pre.preprocess(
        data, 
        variables=variable, 
        q_squared_region=q_squared_region, 
        reconstruction_level="det", 
        signal_only=True
    )
    
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
        x_axis_in_radians(kind="0 to 2pi")

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    file_name = f'q2{q_squared_region}_comp_{variable}.png'

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name=file_name,
    )


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
        bins=approx_num_bins(resolution),
        color="red",
        histtype="step",
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    file_name = f"q2{q_squared_region}_res_{variable}.png"

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name=file_name,
    )
    

def plot_candidate_multiplicity(data, out_dir_path):
    data_det = pre.preprocess(data, reconstruction_level="det")
    data_gen = pre.preprocess(data, reconstruction_level="gen")

    plt.hist(
        data_gen["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=generate_stats_label(data_gen["__event__"], descrp="Generator", show_mean=False, show_rms=False), 
        color="blue", 
        histtype="step"
    )

    plt.hist(
        data_det["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=generate_stats_label(data_det["__event__"], descrp="Detector (after cuts)", show_mean=False, show_rms=False),
        color="red", 
        histtype="step"
    )
    
    plt.title("Candidate Multiplicity")
    plt.xlabel("Candidates per Event")
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.legend()

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name="cand_mult.png",
    )


def max_over_multiple_arrays(ars):
    big_ar = np.concatenate(ars, axis=None)
    max = np.max(big_ar)
    return max


def min_over_multiple_arrays(ars):
    big_ar = np.concatenate(ars, axis=None)
    min = np.min(big_ar)
    return min


def double_hist_2d(
    xs,
    ys,
    num_bins,
):
    assert (len(xs) == 2) and (len(ys) == 2)

    xmax = max_over_multiple_arrays(xs)
    xmin = min_over_multiple_arrays(xs)

    ymax = max_over_multiple_arrays(ys)
    ymin = min_over_multiple_arrays(ys)    

    interval = ((xmin, xmax), (ymin, ymax))

    hists = [np.histogram2d(x, y, bins=num_bins, range=interval) for x, y in zip(xs, ys)]

    return hists



def unzip(zipped_stuff):
    return list(zip(*zipped_stuff))


def multi_array_norm(ars):
    max_counts = max_over_multiple_arrays(ars)
    norm = plt.Normalize(0, max_counts)    
    return norm


def scalar_mappable(norm):
    return mpl.cm.ScalarMappable(norm, cmap='hot')


def subplots_side_by_side():
    fig, axs = plt.subplots(
        ncols=2,
        layout="constrained",
        sharey=True,
    )
    return fig, axs


def plot_hist_2d(ax, hist_2d, norm):
    h = hist_2d[0]
    x_edges = hist_2d[1]
    y_edges = hist_2d[2]
    
    ax.pcolormesh(x_edges, y_edges, h.T, norm=norm, cmap="hot")

    
def plot_hist_2d_side_by_side(
    xs,
    ys,
    num_bins,
    titles, 
    suptitle, 
    supxlabel, 
    supylabel,
):
    
    hists = double_hist_2d(xs, ys, num_bins)
    
    norm = multi_array_norm(unzip(hists)[0])

    sm = scalar_mappable(norm)

    fig, axs = subplots_side_by_side()
    
    for title, hist, ax in zip(titles, hists, axs):

        plot_hist_2d(ax, hist, norm)
        ax.set_title(title)

    plt.colorbar(sm, ax=axs, aspect=30)

    fig.supxlabel(supxlabel)
    fig.supylabel(supylabel)
    fig.suptitle(suptitle)

    return fig, axs


def split_by_q_squared(data):
    split_data = {
        'all': data, 
        'med': data[(data['q_squared'] > 1) & (data['q_squared'] < 6)],
    }
    return split_data


def generate_file_name(plot_name, q_squared_split):
    return f"q2{q_squared_split}_{plot_name}.png"


def find_num_events(data, q_squared_split):
    split_data = split_by_q_squared(data)
    
    num_events = {
        "gen": len(split_data[q_squared_split].loc["gen"]),
        "det": len(split_data[q_squared_split].loc["det"])
    }

    return num_events


def hist_2d_titles_with_count(data, q_squared_split):
    num_events = find_num_events(data, q_squared_split)
    titles = {
        "gen": r"Generator \footnotesize{Count: " + f"{num_events['gen']}" +"}",
        "det": r"Detector \footnotesize{Count: " + f"{num_events['det']}" + "}",
    }
    return titles

    
def hist_2d_costheta_k_p_k(data, q_squared_split, out_dir):

    sig_data = data[data["isSignal"] == 1]

    split_data = split_by_q_squared(sig_data)

    titles = hist_2d_titles_with_count(sig_data, q_squared_split)
    
    plot_hist_2d_side_by_side(
        xs=[
            split_data[q_squared_split].loc["gen"]["costheta_K"],
            split_data[q_squared_split].loc["det"]["costheta_K"],
        ],
        ys=[
            split_data[q_squared_split].loc["gen"]["K_p_p"],
            split_data[q_squared_split].loc["det"]["K_p_p"],
        ],
        num_bins=50,
        titles=[titles["gen"], titles["det"]],
        suptitle=r"Histogram of $\cos\theta_K$ and $p^\text{lab}_K$",
        supxlabel=r"$\cos\theta_K$",
        supylabel=r"$p^\text{lab}_K$",    
    )

    file_name = generate_file_name(
        plot_name = "hist_2d_costheta_k_p_k",
        q_squared_split=q_squared_split
    )

    save_fig_and_clear(
        out_dir_path=out_dir,
        file_name=file_name
    )


def hist_2d_costheta_k_theta_k(data, q_squared_split, out_dir):

    sig_data = data[data["isSignal"] == 1]

    split_data = split_by_q_squared(sig_data)

    titles = hist_2d_titles_with_count(sig_data, q_squared_split)
    
    plot_hist_2d_side_by_side(
        xs=[
            split_data[q_squared_split].loc["gen"]["costheta_K"],
            split_data[q_squared_split].loc["det"]["costheta_K"],
        ],
        ys=[
            split_data[q_squared_split].loc["gen"]["K_p_theta"],
            split_data[q_squared_split].loc["det"]["K_p_theta"],
        ],
        num_bins=50,
        titles=[titles["gen"], titles["det"]],
        suptitle=r"Histogram of $\cos\theta_K$ and $\theta^\text{lab}_K$",
        supxlabel=r"$\cos\theta_K$",
        supylabel=r"$\theta^\text{lab}_K$",    
    )
    
    y_axis_in_radians("0 to pi")
    
    file_name = generate_file_name(
        plot_name = "hist_2d_costheta_k_theta_k",
        q_squared_split=q_squared_split
    )

    save_fig_and_clear(
        out_dir_path=out_dir,
        file_name=file_name
    )

        
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
        print("Plotting efficiency.")
        info = generate_plot_info(
            variables = ["costheta_K", "costheta_mu", "chi"],
            xlabels = [r"$\cos\theta_K$", r"$\cos\theta_\mu$", r"$\chi$"],
            titles = [r"Efficiency of $\cos\theta_K$", r"Efficiency of $\cos\theta_\mu$", r"Efficiency of $\chi$"],
            q_squared_regions = ["all", "med"],
        )
        
        for variable, xlabel, title, q_squared_region in info:
            plot_efficiency(
                data=data,
                variable=variable,
                q_squared_region=q_squared_region,
                num_points=100,
                title=title,
                xlabel=xlabel,
                out_dir_path=out_dir_path,
                mc_truth_comp=True,
            )

    if "resolution" in plots:
        print("Plotting resolution.")
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
        print("Plotting candidate multiplicity.")
        plot_candidate_multiplicity(data, out_dir_path)
    
    if "generics" in plots:
        print("Plotting generics.")
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

    if "helicity vs p theta" in plots:
        print("Plotting helicity angle vs. lab momentum and lab theta.")

        plot_hel_p_theta()

