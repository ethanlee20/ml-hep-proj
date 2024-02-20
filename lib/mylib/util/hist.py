
import numpy as np
import pandas as pd


def make_bin_edges(start, stop, num_bins):
    """Make histogram bin edges."""
    
    bin_size = (stop - start) / num_bins
    return np.arange(start, stop + bin_size, bin_size)


def find_bin_middles(bin_edges):
    """
    Find the position of the middle of each bin.
    
    Note: Assumes uniform bin widths.
    """
    num_bins = len(bin_edges) - 1
    bin_width = (
        np.max(bin_edges) - np.min(bin_edges)
    ) / num_bins
    shifted_edges = bin_edges + 0.5 * bin_width
    return shifted_edges[:-1]
    

def assign_bins(data, bin_edges):
    bins = pd.cut(
        data, 
        bin_edges,
        include_lowest=True
    )
    return bins


def bin_data(data, bins):
    binned = data.groupby(bins)
    return binned


def find_bin_counts(binned):
    """Find the number of entries in each bin."""
    counts = binned.size()
    return counts


def make_q_squared_bins(d_q_squared, bin_edges):
    bins = assign_bins(d_q_squared, bin_edges)
    return bins


