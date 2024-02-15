
"""Efficiency calculations."""


import numpy as np
import pandas as pd

from mylib.util.data import (
    split_by_q_squared, 
    only_signal,
    min_max_over_arrays
)


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
    

def find_bin_counts(data, bin_edges):
    """Find the number of entries of d in each bin."""
    bin_series = pd.cut(
        data,
        bin_edges,
        include_lowest=True,
    )
    data_by_bin = data.groupby(bin_series)
    counts = data_by_bin.size()
    return counts



def calc_eff(data_gen, data_det, num_points):
    """
    Calculate the efficiency per bin.
    
    The efficiency of bin i is defined as the number of
    detector entries in i divided by the number of generator
    entries in i.
    
    The errorbar for bin i is calculated as the squareroot of the
    number of detector entries in i divided by the number of
    generator entries in i.
    """
    min, max = min_max_over_arrays([data_gen, data_det])
    bin_edges = make_bin_edges(start=min, stop=max, num_bins=num_points)
    bin_mids = find_bin_middles(bin_edges)

    bin_count_det = find_bin_counts(data_gen, bin_edges)
    bin_count_gen = find_bin_counts(data_det, bin_edges)
    
    eff = (bin_count_det / bin_count_gen).values
    err = (np.sqrt(bin_count_det) / bin_count_gen).values

    return eff, bin_mids, err


# def calc_eff_check_theta_k_accep(data, var, num_bins, q_squared_split, error_bars=True, mc=False):

#     data = only_signal(data)
#     data = split_by_q_squared(data)[q_squared_split]
#     data_cut = data[(data["K_p_theta"] > 0.25) & (data["K_p_theta"] < 2.625)]

#     if mc:
#         data = data[var+'_mc']
#         data_cut = data_cut[var+'_mc']
#     else:
#         data = data[var]
#         data_cut = data_cut[var]
        
#     bin_edges = make_bin_edges(start=data.min(), stop=data.max(), num_bins=num_bins)

#     bin_count = {
#         "gen": find_bin_counts(data.loc["gen"], bin_edges),
#         "gen_cut": find_bin_counts(data_cut.loc["gen"], bin_edges)
#     }
    
#     eff = (bin_count["gen_cut"] / bin_count["gen"]).values
    
#     bin_middles = find_bin_middles(bin_edges)
    
#     if not error_bars:
#         return eff, bin_middles
    
#     errors = (np.sqrt(bin_count["gen_cut"]) / bin_count["gen"]).values

#     return eff, bin_middles, errors

