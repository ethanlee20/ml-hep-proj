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


 





