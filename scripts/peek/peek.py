import sys

import pandas as pd
pd.options.display.max_columns = None

from mylib.util.util import open_data, open_data_dir

#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/mu_re_00030_job386260858_00_cut_an.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00000_job386260828_00.root'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00001_job386260829_00.root'
# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00003_job388070872_00_cut_an.pkl')
data = open_data_dir('/home/belle2/elee20/ml-hep-proj/data/2024-03-14_gen_mix_e_tf_test/gen_mix_e_tf_test/sub00', tree_names=["gen", "det"])
print(data.head())
# data_gen = data.loc["gen"]
data_det = data.loc["det"]

# print("num gen", len(data_gen))
print("num gen", len(data.loc["gen"]))
print("num det sig", len(data_det[data_det["isSignal"]==1]))
print("num det bkg", len(data_det[data_det["isSignal"]==0]))
print("num det tot", len(data_det))
# print(data.columns.values.tolist())
# print(data["mcPDG"])
