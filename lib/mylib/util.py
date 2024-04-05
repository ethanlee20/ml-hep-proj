import sys
import pathlib as pl
from warnings import simplefilter

from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import uproot
import pandas as pd

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)



"""Constants"""
q_squared_splits = ["med", "all"]



"""Misc."""
def unzip(zipped_stuff):
    return list(zip(*zipped_stuff))


def unzip_dicts(a:list):
    """Unzip a list of dictionaries with the same keys."""
    keys = a[0].keys()
    values = unzip([i.values() for i in a])
    return dict(zip(keys, values))
    


"""File handling"""

def open_tree(file_path, tree_name):
    df = uproot.open(f"{file_path}:{tree_name}").arrays(library="pd")
    return df


def open_root(file_path, tree_names):
	dfs = [
		open_tree(file_path, tree_name) 
		for tree_name in tree_names
	]
	print(f"opened {file_path}")
	return pd.concat(dfs, keys=tree_names)


def open_data_file(file_path, tree_names=None):
    file_path = pl.Path(file_path)
    if file_path.suffix == ".root":
        return open_root(file_path, tree_names) 
    print(f"opening {file_path}")
    return pd.read_pickle(file_path)


def open_data_dir(path, tree_names=None):
    path = pl.Path(path)
    file_paths = list(path.glob('*.root')) + list(path.glob('*.pkl'))
    dfs = [open_data_file(path, tree_names) for path in file_paths]
    return pd.concat(dfs)


def open_data(paths, tree_names=["gen", "det"]):
    def _open(path):
        path = pl.Path(path)
        if path.suffix in {".root", ".pkl"}:
            data = open_data_file(path, tree_names=tree_names) 
        else: data = open_data_dir(path, tree_names=tree_names) 
        return data
    
    if type(paths) is list:
        datas = [_open(path) for path in paths]
        data = pd.concat(datas)
        return data
    
    path = pl.Path(paths)
    data = _open(path)
    return data



"""Data Manipulations"""

def min_max_over_arrays(ars:list):
    big_ar = np.concatenate(ars, axis=None)
    min = np.nanmin(big_ar)
    max = np.nanmax(big_ar)
    return min, max   


def count_events(dat_ser):
    num_events = len(dat_ser)
    return num_events


def sig_(data):
    isSignal = data["isSignal"]==1
    return data[isSignal]


def noise_(data):
    isNoise = data["isSignal"]!=1
    return data[isNoise]

    
def split_by_q_squared(data, split):
    if split == 'all':
        return data
    elif split == 'med':
        return data[(data['q_squared'] > 1) & (data['q_squared'] < 6)]
    elif split == 'JPsi':
        return  data[(data['q_squared'] > 8) & (data['q_squared'] < 11)]
    else:
        raise ValueError()


def section(data, sig_noise=None, var=None, q_squared_split=None, gen_det=None):
    if sig_noise == "sig":
        data = sig_(data)
    elif sig_noise == "noise":
        data = noise_(data)

    if q_squared_split:
        data = split_by_q_squared(data, q_squared_split)

    if var:
        data = data[var]

    if gen_det == "gen":
        data = data.loc[["gen"]]
    elif gen_det == "det":
        data = data.loc[["det"]]
    
    return data


def veto_q_squared_mix_bkg(data):
    veto_j_psi = ~((data['q_squared'] > 8) & (data['q_squared'] < 11)) 
    data = data[veto_j_psi]
    veto_psi_2s = ~((data['q_squared'] > 12.75) & (data['q_squared'] < 14))
    data = data[veto_psi_2s]
    return data



"""Iterations"""

def over_q_squared_splits(f):
    def wrapper(*args, **kwargs):
        for q_squared_split in q_squared_splits:
            f(*args, q_squared_split=q_squared_split, **kwargs)
    return wrapper



"""Histogram"""

def approx_num_bins(data):
    """Approximate the number of bins for a histogram by the length of the data."""
    return round(np.sqrt(len(data)))


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


"""Testing"""

test_df_a = pd.DataFrame(
    {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]},
    index=[3, 4, 10],
)


test_df_b = pd.DataFrame(
    {"d": [1, 1, 2], "e": [3, 2, 1], "f": [5, 4, 7]},
    index=[3, 4, 10],
)


test_df_c = pd.DataFrame(
    {"d": [1, 1, 2, 7, 6, 3, 1, 4, 5, 2], "e": [3, 2, 1, 4, 10, 2, 4, 4, 5, 1]},
    index=[3, 4, 10, 11, 13, 14, 15, 16, 18, 20]
)

test_df_d = pd.DataFrame(
    {"d": [1, 2, 3, 2, 8, 1, 4, 5, 5, 2], "e": [3, 2, 1, 4, 10, 2, 4, 4, 5, 1]},
    index=[3, 4, 10, 11, 13, 14, 15, 16, 18, 20]
)

test_df_vec_a = pd.DataFrame(
    {"v_1": [2, 5, 3], "v_2": [7, 12, 1], "v_3": [1, 4, 2]},
    index=[1, 5, 6],
)


test_df_vec_b = pd.DataFrame(
    {"v_1": [4, 5, 1], "v_2": [1, 2, 5], "v_3": [7, 1, 4]},
    index=[1, 5, 6],
)


test_df_square_mat = pd.DataFrame(
    {
        "m_11": [4, 1, 3],
        "m_12": [6, 1, 4],
        "m_13": [8, 5, 5],
        "m_21": [7, 4, 2],
        "m_22": [1, 0, 8],
        "m_23": [7, 10, 4],
        "m_31": [6, 4, 2],
        "m_32": [9, 3, 2],
        "m_33": [9, 2, 7],
    },
    index=[1, 5, 6],
)


test_df_4vec_a = pd.DataFrame(
    {
        "v_1": [1, 5, 4],
        "v_2": [5, 2, 4],
        "v_3": [8, 9, 5],
        "v_4": [1, 5, 3],
    },
    index=[4, 6, 9],
)


test_df_4mom_a = pd.DataFrame(
    {
        "E": [1, 5, 4],
        "px": [5, 2, 4],
        "py": [8, 9, 5],
        "pz": [1, 5, 3],
    },
    index=[4, 6, 9],
)


test_df_4mom_b = pd.DataFrame(
    {
        "E": [3, 2, 3],
        "px": [1, 4, 3],
        "py": [1, 4, 2],
        "pz": [0, 2, 5],
    },
    index=[4, 6, 9],
)
