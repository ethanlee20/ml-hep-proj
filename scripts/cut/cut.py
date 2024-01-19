import sys
import pathlib as pl

import pandas as pd

import mylib
    

def configure_data_paths(data_dir_path):

    raw_data_dir_name = "sub00/"
    raw_data_dir_path = data_dir_path.joinpath(raw_data_dir_name)
    raw_data_file_paths = list(raw_data_dir_path.glob("*.root"))

    cut_data_dir_name = "cut/"
    cut_data_dir_path = data_dir_path.joinpath(cut_data_dir_name)
    cut_data_dir_path.mkdir(parents=True, exist_ok=True)
    
    cut_data_file_paths = [
        cut_data_dir_path.joinpath(f"{path.stem}_cut.pkl")
        for path in raw_data_file_paths
    ]
    
    return raw_data_file_paths, cut_data_file_paths


def configure_plot_path(data_dir_path):

    plots_dir_name = "plots"

    plots_dir_path = data_dir_path.joinpath(plots_dir_name)
    plots_dir_path.mkdir(parents=True, exist_ok=True)

    return plots_dir_path


def load_data(file_path):
    return mylib.open(file_path, ['gen', 'det'])
    

def apply_cuts(df, plots_dir_path):

    df_gen_uncut = df.loc['gen']

    df_det_cut = mylib.apply_all_cuts(
        df.loc['det'],
        plots_dir_path
    )

    return pd.concat([df_gen_uncut, df_det_cut], keys=['gen', 'det'])


def save(df, out_file_path):
    df.to_pickle(out_file_path)


def main():

    data_dir_path = pl.Path("/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/")
 
    raw_data_file_paths, cut_data_file_paths = configure_data_paths(data_dir_path)

    plots_dir_path = configure_plot_path(data_dir_path)

    for raw_path, cut_path in zip(raw_data_file_paths, cut_data_file_paths):
        df = load_data(raw_path)

        df_cut = apply_cuts(df, plots_dir_path)

        save(df_cut, cut_path)


if __name__ == "__main__":
    main()
