
import pathlib as pl

import numpy as np
import pandas as pd

from mylib.util.util import open_data
from mylib.pre.cuts import apply_all_cuts_with_summary, make_total_count_summary    


def config_paths(in_dir, out_dir):
    in_dir = pl.Path(in_dir)
    out_dir = pl.Path(out_dir)

    in_data_paths = list(in_dir.glob('*.root'))
    out_data_paths = [out_dir.joinpath(f'{in_path.stem}_cut.pkl') 
                      for in_path in in_data_paths]
    out_summ_paths = [out_dir.joinpath(f'{in_path.stem}_cut_summ.csv')
                      for in_path in in_data_paths]

    return in_data_paths, out_data_paths, out_summ_paths


def apply_cuts(df):
    df_gen_uncut = df.loc['gen']
    df_det_cut, summ = apply_all_cuts_with_summary(
        df.loc['det'],
    )
    cut_df = pd.concat([df_gen_uncut, df_det_cut], keys=['gen', 'det'])
    return cut_df, summ


def main():

    input_dir = '/home/belle2/elee20/ml-hep-proj/data/2024-03-11_genericMu/genericMu/sub00'
    # input_dir = '/home/belle2/elee20/ml-hep-proj/data/2024-03-07_gridbdtmu/subset/mc'
    output_dir = '/home/belle2/elee20/ml-hep-proj/data/2024-03-11_genericMu/genericMu/cut'
    # output_dir = '/home/belle2/elee20/ml-hep-proj/data/2024-03-07_gridbdtmu/subset/cut'
    
    input_paths, output_paths, summ_paths = config_paths(input_dir, output_dir)

    for in_path, out_path, summ_path in zip(input_paths, output_paths, summ_paths):
        data = open_data(in_path, tree_names=['gen', 'det'])
        cut_data, summ = apply_cuts(data)
        cut_data.to_pickle(out_path)
        summ.to_csv(summ_path)

    tot_summ = make_total_count_summary(output_dir)
    np.savetxt(f'{output_dir}/tot_cut_summ.txt', tot_summ, fmt="%i")

if __name__ == "__main__":
    main()
