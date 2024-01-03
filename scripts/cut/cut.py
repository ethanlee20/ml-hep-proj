import os.path
import sys

import pandas as pd

import mylib


# configure paths

data_dir = sys.argv[1]
input_filename = "mc_events_mu_reconstructed.root"
input_filepath = os.path.join(data_dir, input_filename)

output_generator_data_filename = "mc_events_mu_reconstructed_gen_uncut.pkl"
output_detector_data_filename = "mc_events_mu_reconstructed_det_cut.pkl"

output_generator_data_path = os.path.join(data_dir, output_generator_data_filename)
output_detector_data_path = os.path.join(data_dir, output_detector_data_filename)


# load data 

df_det_uncut = mylib.open_tree(input_filepath+':det')
df_gen_uncut = mylib.open_tree(input_filepath+':gen')

df_det_cut = mylib.apply_all_cuts(df_det_uncut)


# save output
df_det_cut.to_pickle(output_detector_data_path)
df_gen_uncut.to_pickle(output_generator_data_path)

