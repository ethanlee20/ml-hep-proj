import os.path
import sys
import pathlib as pl

import pandas as pd

import mylib


def configure_data_paths():

	data_dir_path = pl.Path(sys.argv[1])

	in_file_names = [
    	pl.Path(file_name) for file_name in sys.argv[2:]
	]
	
	in_file_paths = [
    	data_dir_path.joinpath(file_name)
    	for file_name in in_file_names
	]

	out_file_names = [
		file_name.stem + "_cut" + file_name.suffix for file_name in in_file_names
  	] 

	out_file_paths = [
		data_dir.joinpath(file_name) 
		for file_name in out_file_names
	]
	
	return data_dir_path, in_file_paths, out_file_paths


def configure_plot_paths(data_dir_path):

	plots_dir_name = "plots"
	cut_plots_dir_name = "cuts"

	plots_dir_path = data_dir.joinpath(plots_dir_name)
	cut_plots_dir_path = plots_dir_path.joinpath(
	    cut_plots_dir_name
	)

	cut_plots_dir_path.mkdir(parents=True, exist_ok=True)

	return cut_plots_dir_path


def load_data(in_file_path):
	return mylib.open_root(in_file_path, ['gen', 'det'])
	

def apply_cuts(df, cut_plots_dir_path):

	df_det_cut = mylib.apply_all_cuts(
	    df['det'], cut_plots_dir_path
	)

	df_gen_uncut = df['gen']

	df_cut = pd.concat([df_gen_uncut, df_det_cut], keys=['gen', 'det'])

	return df_cut
	

def save(df, out_file_path):
	df.to_pickle(out_file_path)


def main():
	data_dir_path, in_file_paths, out_file_paths = configure_data_paths()

	cut_plots_dir_path = configure_plot_paths(data_dir_path)

	for in_path, out_path in zip(in_file_paths, out_file_paths):

		df = load_data(in_path)

		apply_cuts(df, cut_plots_dir_path)

		save(df, out_path)


if __name__ == "__main__":
	main()
