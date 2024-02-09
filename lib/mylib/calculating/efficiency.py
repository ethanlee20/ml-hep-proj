
import numpy as np
from mylib.utilities.data import split_by_q_squared, only_signal


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


def calculate_efficiency(data, var, num_bins, q_squared_split, error_bars=True, mc=False):
    """
    Calculate the efficiency per bin.
    
    The efficiency of bin i is defined as the number of
    detector entries in i divided by the number of generator
    entries in i.
    
    The errorbar for bin i is calculated as the squareroot of the
    number of detector entries in i divided by the number of
    generator entries in i.
    """
    # if mc:
    #     data_det = pre.preprocess(data, variables=variable+"_mc", q_squared_split=q_squared_split, reconstruction_level="det", signal_only=True)
    # else:
    #     data_det = pre.preprocess(data, variables=variable, q_squared_split=q_squared_split, reconstruction_level="det", signal_only=True)
    # data_gen = pre.preprocess(data, variables=variable, q_squared_split=q_squared_split, reconstruction_level="gen")

    data = only_signal(data)
    data = split_by_q_squared(data)[q_squared_split]
    if mc:
        data = data[var+'_mc']
    else:
        data = data[var]
        

    bin_edges = generate_bin_edges(start=data.min(), stop=data.max(), num_of_bins=num_bins)

    bin_count = {
        "gen": find_bin_counts(data.loc["gen"], bin_edges),
        "det": find_bin_counts(data.loc["det"], bin_edges)
    }
    
    eff = (bin_count["det"] / bin_count["gen"]).values
    
    bin_middles = find_bin_middles(bin_edges)
    
    if not error_bars:
        return eff, bin_middles
    
    errors = (np.sqrt(bin_count["det"]) / bin_count["gen"]).values

    return eff, bin_middles, errors

