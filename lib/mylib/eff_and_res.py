
import itertools

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import preprocess as pre


def generate_bin_edges(start, stop, num_of_bins):
    """Generate histogram bin edges."""
    
    bin_size = (stop - start) / num_of_bins
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
    

def find_bin_counts(data_series, bin_edges):
    """Find the numbers of entries in each bin."""
    bin_series = pd.cut(
        data_series,
        bin_edges,
        include_lowest=True,
    )
    data_by_bin = data_series.groupby(bin_series)
    counts = data_by_bin.size()
    return counts


def calculate_efficiency(data, variable, num_bins, q_squared_region, error_bars=True, mc=False):
    """
    Calculate the efficiency per bin.
    
    The efficiency of bin i is defined as the number of
    detector entries in i divided by the number of generator
    entries in i.
    
    The errorbar for bin i is calculated as the squareroot of the
    number of detector entries in i divided by the number of
    generator entries in i.
    """
    if mc:
        data_det = pre.preprocess(data, variables=variable+"_mc", q_squared_region=q_squared_region, reconstruction_level="det", signal_only=True)
    else:
        data_det = pre.preprocess(data, variables=variable, q_squared_region=q_squared_region, reconstruction_level="det", signal_only=True)
    data_gen = pre.preprocess(data, variables=variable, q_squared_region=q_squared_region, reconstruction_level="gen")

    data_min = min(data_det.min(), data_gen.min())
    data_max = max(data_det.max(), data_gen.max())
    bin_edges = generate_bin_edges(start=data_min, stop=data_max, num_of_bins=num_bins)

    bin_counts_detector = find_bin_counts(
        data_det, bin_edges
    )
    bin_counts_generator = find_bin_counts(
        data_gen, bin_edges
    )
    
    eff = (bin_counts_detector / bin_counts_generator).values
    
    bin_middles = find_bin_middles(bin_edges)
    
    if not error_bars:
        return eff, bin_middles
    
    errors = (np.sqrt(bin_counts_detector) / bin_counts_generator).values

    return eff, bin_middles, errors


def calculate_resolution(data, variable, q_squared_region):
    """
    Calculate the resolution.
    
    The resolution of a variable is defined as the 
    reconstructed value minus the MC truth value.
    """
    data_calc = pre.preprocess(data, variable=variable, q_squared_region=q_squared_region, reconstruction_level="det", signal_only=True)
    data_mc = pre.preprocess(data, variable=variable+'_mc', q_squared_region=q_squared_region, reconstruction_level="det", signal_only=True)
    
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



    
    
