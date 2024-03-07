
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from mylib.util.data import min_max_over_arrays
from mylib.plot.core.subplots import subplots_side_by_side
from mylib.util.util import unzip_dicts

cmap = 'hot'


def multi_hist_norm(hists):
    _, max_counts = min_max_over_arrays(hists)
    norm = plt.Normalize(0, max_counts)    
    return norm


def scalar_mappable(norm):
    return mpl.cm.ScalarMappable(norm, cmap=cmap)


def calc_multi_hist_2d(
    xs: list,
    ys: list,
    num_bins: int,
):
    assert len(xs) == len(ys)
  
    xmin, xmax = min_max_over_arrays(xs)
    ymin, ymax = min_max_over_arrays(ys)
    interval = ((xmin, xmax), (ymin, ymax))
    hists = [np.histogram2d(x, y, num_bins, interval) for x, y in zip(xs, ys)]
    
    return hists

    
def plot_hist_2d(ax, hist_2d, norm):
    x_edges = hist_2d[0]
    y_edges = hist_2d[1]
    h = hist_2d[2]
    ax.pcolormesh(
        x_edges, 
        y_edges, 
        h.T, 
        norm=norm, 
        cmap=cmap
    )


def plot_hist_2d_side_by_side(
    xs,
    ys,
    num_bins,
):
    assert((len(xs) == 2) & (len(ys) == 2))

    hists = calc_multi_hist_2d(xs, ys, num_bins)
    hs = unzip_dicts(hists)[2]
    norm = multi_hist_norm(hs)

    fig, axs = subplots_side_by_side()
    for hist, ax in zip(hists, axs):
        plot_hist_2d(ax, hist, norm)

    return fig, axs, norm


def add_color_bar(axs, norm):
    sm = scalar_mappable(norm)
    plt.colorbar(sm, ax=axs, aspect=30)
    
