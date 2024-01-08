
import sys
import pathlib as pl

import pandas as pd

import mylib


def configure_paths():
	data_dir_path = pl.Path(sys.argv[1])

	in_file_names = sys.argv[3:]

	in_file_paths = [data_dir_path.joinpath(file_name) for file_name in in_file_names]

	out_file_name = sys.argv[2]
	
	out_file_path = data_dir_path.joinpath(out_file_name)

	return in_file_paths, out_file_path


def combine_data(in_file_paths):
 
	dfs = [mylib.open_root(path, ['gen', 'det']) for path in in_file_paths]	
	return pd.concat(dfs)
	

def main():
	in_file_paths, out_file_path = configure_paths()

	big_df = combine_data(in_file_paths)

	big_df.to_pickle(out_file_path)


if __name__ == "__main__":
	main()
