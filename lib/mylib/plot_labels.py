import matplotlib.pyplot as plt
import numpy as np


def set_plot_labels(
    fig, 
    axs, 
    titles=None, 
    xlabels=None, 
    ylabels=None, 
    suptitle=None, 
    supxlabel=None, 
    supylabel=None,
):
    for ax, title in zip(axs, titles):
        ax.set_title(title)
    for ax, xlabel in zip(axs, xlabels):
        ax.set_xlabel(xlabel)
    for ax, ylabel in zip(axs, ylabels):
        ax.set_ylabel(ylabel)
        
    fig.suptitle(suptitle)
    fig.supxlabel(supxlabel)
    fig.supylabel(supylabel)


def ticks_in_radians(axis, kind):
    if axis == "x":
        ticks_fn = plt.xticks
    elif axis == "y":
        ticks_fn = plt.yticks
        
    if kind == "0 to 2pi":
        ticks_fn(
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
        ticks_fn(
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
