
import pathlib as pl
import argparse
from mylib.util import open_data

parser = argparse.ArgumentParser()
parser.add_argument('in_path')
parser.add_argument('out_path')
args = parser.parse_args()

in_path = pl.Path(parser.in_path)
out_path = pl.Path(parser.out_path)


data = open_data(in_path)

data.to_pickle(out_path)