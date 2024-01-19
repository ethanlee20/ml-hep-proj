
import sys
import pathlib as pl

import pandas as pd

import mylib



def configure_paths(data_dir_path, out_file_name):

    in_file_paths = [str(path) for path in list(data_dir_path.glob("*.root"))]
#    in_file_paths = [
#        '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00000_job386260828_00.root',
#        '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00001_job386260829_00.root'
#    ]
    out_file_path = data_dir_path.joinpath(out_file_name)

    return in_file_paths, out_file_path


def combine_data(in_file_paths):
 
    dfs = [mylib.open_root(path, ['gen', 'det']) for path in in_file_paths] 
    return pd.concat(dfs)
    

def main():

    data_dir_path = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/')

    out_file_name = "mu_re.pkl"

    in_file_paths, out_file_path = configure_paths(data_dir_path, out_file_name)

    big_df = combine_data(in_file_paths)

    big_df.to_pickle(out_file_path)


if __name__ == "__main__":
    main()
