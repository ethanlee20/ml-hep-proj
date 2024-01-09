import sys
print(sys.path)

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


def check_root(file_path, tree_names):
    df = open_root(file_path, tree_names)
    print(df.head(6))
    print("length: ", len(df))


def check_columns_root(path):
    df = open_tree(path)
    print("columns: ")
    print(df.columns.values.tolist())
