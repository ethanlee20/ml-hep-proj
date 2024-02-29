import sys
import pathlib as pl
from warnings import simplefilter

import numpy as np
import uproot
import pandas as pd

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def unzip(zipped_stuff):
    return list(zip(*zipped_stuff))


def unzip_dicts(a:list):
    """Unzip a list of dictionaries with the same keys."""
    keys = a[0].keys()
    values = unzip([i.values() for i in a])
    return dict(zip(keys, values))
    

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


def open_data(file_path, tree_names=None):
    file_path = pl.Path(file_path)
    if file_path.suffix == ".root":
        return open_root(file_path, tree_names) 
    print(f"opening {file_path}")
    return pd.read_pickle(file_path)


def open_data_dir(path, tree_names=None):
    path = pl.Path(path)
    file_paths = list(path.glob('[!.]*'))
    dfs = [open_data(path, tree_names) for path in file_paths]
    return pd.concat(dfs)


def check_root(file_path, tree_names):
    df = open_root(file_path, tree_names)
    print(df.head(6))
    print("length: ", len(df))


def check_columns_root(path):
    df = open_tree(path)
    print("columns: ")
    print(df.columns.values.tolist())


 





