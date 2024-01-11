import sys
import pathlib as pl

import uproot

import pandas as pd


# Utilities


def open_tree(file_path, tree_name):
    df = uproot.open(f"{file_path}:{tree_name}").arrays(library="pd")
    return df


def open_root(file_path, tree_names):
	dfs = [
		open_tree(file_path, tree_name) 
		for tree_name in tree_names
	]
	print(len(dfs))
	return pd.concat(dfs, keys=tree_names)

def open(file_path, tree_names=None):
    file_path = pl.Path(file_path)
    if file_path.suffix == ".root":
        return open_root(file_path, tree_names) 
    return pd.read_pickle(file_path)

def check_root(file_path, tree_names):
    df = open_root(file_path, tree_names)
    print(df.head(6))
    print("length: ", len(df))


def check_columns_root(path):
    df = open_tree(path)
    print("columns: ")
    print(df.columns.values.tolist())
