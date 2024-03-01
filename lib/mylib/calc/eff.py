
"""Efficiency calculations."""


import numpy as np
import pandas as pd

from mylib.util.data import (
    min_max_over_arrays
)
from mylib.util.hist import (
    bin_data,
    make_bin_edges,
    find_bin_middles,
    find_bin_counts,
)



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

    binned_gen = bin_data(data_gen, bin_edges)
    binned_det = bin_data(data_det, bin_edges)

    bin_count_det = find_bin_counts(binned_gen)
    bin_count_gen = find_bin_counts(binned_det)
    
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

