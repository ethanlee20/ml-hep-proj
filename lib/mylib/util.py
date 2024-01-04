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


def check_columns_root(path):
    df = open_tree(path)
    print("columns: ")
    print(df.columns.values.tolist())
