import pathlib as pl

import matplotlib as mpl
import matplotlib.pyplot as plt


def approx_num_bins(data_series):
    return round(np.sqrt(len(data_series)))


def multi_hist_norm(hs):
    max_counts = max_over_multiple_arrays(hs)
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


