
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from mylib.utilities.util import min_max_over_multiple_arrays, unzip_dicts
from mylib.plotting.core.subplots import subplots_side_by_side


def multi_hist_norm(hs):
    _, max_counts = min_max_over_multiple_arrays(hs)
    norm = plt.Normalize(0, max_counts)    
    return norm


def scalar_mappable(norm):
    return mpl.cm.ScalarMappable(norm, cmap='hot')


def calc_hist_2d(x, y, bins, range):
    h, x_edges, y_edges = np.histogram2d(x, y, bins, range)    
    return {"h":h, "x_edges":x_edges, "y_edges":y_edges}


def calc_multi_hist_2d(
    xs: list,
    ys: list,
    num_bins: int,
):
    assert len(xs) == len(ys)
  
    xmin, xmax = min_max_over_multiple_arrays(xs)
    ymin, ymax = min_max_over_multiple_arrays(ys)
    interval = ((xmin, xmax), (ymin, ymax))

    hists = [calc_hist_2d(x, y, bins=num_bins, range=interval) for x, y in zip(xs, ys)]
    return hists

    
def plot_hist_2d(ax, hist_2d, norm):
    ax.pcolormesh(
        hist2d["x_edges"], 
        hist2d["y_edges"], 
        hist2d["h"].T, 
        norm=norm, 
        cmap="hot"
    )


def plot_hist_2d_side_by_side(
    xs,
    ys,
    num_bins,
):
    assert((len(xs) == 2) & (len(ys) == 2))

    hists = calc_multi_hist_2d(xs, ys, num_bins)
    norm = multi_hist_norm(unzip_dicts(hists)["h"])

    fig, axs = subplots_side_by_side()
    for hist, ax in zip(hists, axs):
        plot_hist_2d(ax, hist, norm)

    return fig, axs, norm


def add_color_bar(axs, norm):
    sm = scalar_mappable(norm)
    plt.colorbar(sm, ax=axs, aspect=30)
    

def plot_hist_2d_side_by_side_full(
    xs,
    ys,
    num_bins,
    titles,
    suptitle,
    supxlabel,
    supylabel,    
):
    fig, axs, norm = plot_hist_2d_side_by_side(xs, ys, num_bins)
    add_color_bar(axs, norm)
    set_plot_labels(
        fig, 
        axs, 
        titles=titles, 
        suptitle=suptitle, 
        supxlabel=supxlabel, 
        supylabel=supylabel
    )
    return fig, axs


def title_with_count(data, q_squared_split, reconstruction_level, only_signal):
    num_events = find_num_events(data, q_squared_split, reconstruction_level, only_signal)

    if reconstruction_level == "gen":
        label = "Generator"
    elif reconstruction_level == "det":
        label = "Detector"

    title = label + r"\footnotesize{Count: " + f"{num_events}" + "}"    
    return title


def titles_with_count(data, q_squared_split, only_signal):
    titles = {
        level: title_with_count(
            data=data, 
            q_squared_split=q_squared_split, 
            reconstruction_level=level, 
            only_signal=only_signal
         ) for level in data_util.reconstruction_levels
    }
    return titles


def plot_hist_2d_vars(
    data,
    var_x,
    var_y,
    q_squared_split,
    only_signal,
    suptitle,
    supxlabel,
    supylabel,
):
    split_data = data_util.split(data, only_signal=only_signal)
    titles = titles_with_count(data, q_squared_split, only_signal=only_signal)

    fig, axs = plot_hist_2d_side_by_side_full(
        xs=[
            split_data[q_squared_split].loc["gen"][var_x],
            split_data[q_squared_split].loc["det"][var_x],
        ],
        ys=[
            split_data[q_squared_split].loc["gen"][var_y],
            split_data[q_squared_split].loc["det"][var_y],
        ],
        num_bins=50,
        titles=[titles["gen"], titles["det"]],
        suptitle=suptitle,
        supxlabel=supxlabel,
        supylabel=supylabel,
    )
    return fig, axs
    

    
    
