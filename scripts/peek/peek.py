import sys

import pandas as pd
pd.options.display.max_columns = None

from mylib.util.util import open_data, open_data_dir

#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/mu_re_00030_job386260858_00_cut_an.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00000_job386260828_00.root'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00001_job386260829_00.root'
# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00003_job388070872_00_cut_an.pkl')
data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-12_test_e/e_test4/sub00/e_re_00038_job397107227_00.root', tree_names=["gen", "det"])
print(data.loc["gen"].head())
print(len(data[data["isSignal"]==1]))
print(len(data[data["isSignal"]==0]))
# print(data.columns.values.tolist())
# print(data["mcPDG"])
