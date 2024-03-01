
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
    
    
def bin_data(df, var, num_bins, ret_edges=False):
    """Bin data in specified variable (equal size bins)."""

    bin_edges = make_bin_edges(
        start=df[var].min(), 
        stop=df[var].max(), 
        num_bins=num_bins
    )
    bins = pd.cut(df[var], bin_edges, include_lowest=True)
    binned = df.groupby(bins)

    if ret_edges == False:
        return binned
    return binned, bin_edges


def find_bin_counts(binned):
    """Find the number of entries in each bin."""
    counts = binned.size()
    return counts


