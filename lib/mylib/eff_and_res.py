
import itertools

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_bin_edges(start, stop, num_of_bins):
    bin_size = (stop - start) / num_of_bins
    return np.arange(start, stop + bin_size, bin_size)


def find_bin_middles(bin_edges):
    """Assumes uniform bin widths"""
    num_bins = len(bin_edges) - 1
    bin_width = (
        np.max(bin_edges) - np.min(bin_edges)
    ) / num_bins
    shifted_edges = bin_edges + 0.5 * bin_width
    return shifted_edges[:-1]


def find_bin_counts(data, binning_variable, bin_edges):
    bin_series = pd.cut(
        data[binning_variable],
        bin_edges,
        include_lowest=True,
    )
    data_by_bin = data.groupby(bin_series)
    counts = data_by_bin.size()
    return counts


def calculate_efficiency(data1, data2, variable, bin_edges):
    bin_counts_data1 = find_bin_counts(
        data1, variable, bin_edges
    )
    bin_counts_data2 = find_bin_counts(
        data2, variable, bin_edges
    )
    return (bin_counts_data1 / bin_counts_data2).values


def calculate_efficiency_errorbars(
    data1, data2, variable, bin_edges
):
    bin_counts_data1 = find_bin_counts(
        data1, variable, bin_edges
    )
    bin_counts_data2 = find_bin_counts(
        data2, variable, bin_edges
    )
    return (
        np.sqrt(bin_counts_data1) / bin_counts_data2
    ).values


def apply_q_squared_split(split, data):
    if split == "med":
        return data[(data['q_squared']>1)&(data['q_squared']<6)]
    elif split == "all":
        return data
    else: print(f"Unrecognized split: {split}")


def calculate_resolution(variable, q_squared_split, data):

    signal_data = data[data["isSignal"]==1]

    signal_data = apply_q_squared_split(q_squared_split, signal_data)
    
    mc_variable = variable + '_mc'
    
    resolution = signal_data[variable] - signal_data[mc_variable]

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


def calculate_resolutions(variables, q_squared_splits, data):

    calc_info = [
        dict(var=var, split=split) 
        for var, split 
        in itertools.product(variables, q_squared_splits)
    ]
     
    resolutions = [
        calculate_resolution(*info.values(), data)
        for info
        in calc_info    
    ]
    return zip(resolutions, calc_info)


    
    
