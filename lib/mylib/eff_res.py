

import numpy as np
import pandas as pd

from mylib.util import (
    section,
    min_max_over_arrays,
    bin_data,
    make_bin_edges,
    find_bin_middles,
    find_bin_counts,
)


"""Efficiency calculations."""

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

    bin_count_gen = find_bin_counts(binned_gen)
    bin_count_det = find_bin_counts(binned_det)
    
    eff = (bin_count_det / bin_count_gen).values
    err = (np.sqrt(bin_count_det) / bin_count_gen).values
    
    return eff, bin_mids, err



"""Resolution calculations."""

def calculate_resolution(data, variable, q_squared_split):
    """
    Calculate the resolution.
    
    The resolution of a variable is defined as the 
    reconstructed value minus the MC truth value.
    """
    data_calc = section(data, only_sig=True, var=variable, q_squared_split=q_squared_split).loc["det"]
    data_mc = section(data, only_sig=True, var=variable+'_mc', q_squared_split=q_squared_split).loc["det"]
    
    resolution = data_calc - data_mc

    if variable != "chi":
        return resolution

    def apply_periodicity(resolution):
        resolution = resolution.where(
                resolution < np.pi, resolution - 2 * np.pi
        )
        resolution = resolution.where(
            resolution > -np.pi, resolution + 2 * np.pi
        )
        return resolution

    return apply_periodicity(resolution)

