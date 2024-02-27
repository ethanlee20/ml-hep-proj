
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from mylib.util.data import min_max_over_arrays
from mylib.plot.core.subplots import subplots_side_by_side
from mylib.util.util import unzip_dicts


def multi_hist_norm(hs):
    _, max_counts = min_max_over_arrays(hs)
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
  
    xmin, xmax = min_max_over_arrays(xs)
    ymin, ymax = min_max_over_arrays(ys)
    interval = ((xmin, xmax), (ymin, ymax))

    hists = [calc_hist_2d(x, y, bins=num_bins, range=interval) for x, y in zip(xs, ys)]
    return hists

    
def plot_hist_2d(ax, hist_2d, norm):
    ax.pcolormesh(
        hist_2d["x_edges"], 
        hist_2d["y_edges"], 
        hist_2d["h"].T, 
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
    
