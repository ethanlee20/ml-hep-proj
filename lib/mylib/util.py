import uproot
import numpy as np

# Utilities


def open_tree(path):
    df = uproot.open(path).arrays(library="pd")
    return df


def check_root(path):
    df = open_tree(path)
    print(df.head(6))
    print("length: ", len(df))


def generate_bin_edges(start, stop, num_of_bins):
    bin_size = (stop - start) / num_of_bins
    return np.arange(start, stop + bin_size, bin_size)
