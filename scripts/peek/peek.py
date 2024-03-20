import sys
import pathlib as pl

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util.util import open_data, open_data_dir

#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/mu_re_00030_job386260858_00_cut_an.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00000_job386260828_00.root'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00001_job386260829_00.root'
# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00003_job388070872_00_cut_an.pkl')


def open_data(path):
    path = pl.Path(path)
    if path.suffix in {".root", ".pkl"}:
        data = open_data(path, tree_names=["gen", "det"])
    else: data = open_data_dir(path, tree_names=["gen", "det"])
    return data


def print_column_names(data):
    print(data.columns.values)


def print_mc_particles(data):
    for cand in range(len(data)):
        print(data["__MCDecayString__"].iloc[cand])


def print_counts(data):
    isSignal = (data["isSignal"]==1) & (data["KST0_isSignal"]==1) & (data["K_p_isSignal"]==1) & (data["pi_m_isSignal"]==1) & (data["e_p_isSignal"]==1) & (data["e_m_isSignal"]==1)
    isBkg = (data["isSignal"]==0) | (data["KST0_isSignal"]==0) | (data["K_p_isSignal"]==0) | (data["pi_m_isSignal"]==0) | (data["e_p_isSignal"]==0) | (data["e_m_isSignal"]==0)

    print("num gen", len(data.loc["gen"]))
    print("num det sig", len(data[isSignal].loc["det"]))
    print("num det bkg", len(data[isBkg].loc["det"]))
    print("num det tot", len(data.loc["det"]))



data = open_data("/home/belle2/elee20/ml-hep-proj/data/2024-03-19_gen_mix_e_print_test/gen_mix_e_print5/sub00")
print_column_names(data)
print_counts(data)

# data.index = pd.MultiIndex.from_tuples(data.index)

# print(data.head())
# print(data.loc["det"].head())

# print("num gen", len(data_gen))
# print("num gen", len(data.loc["gen"]))
# print("num det sig", len(data_det[data_det["isSignal"]==1]))
# print("num det bkg", len(data_det[data_det["isSignal"]==0]))
# print("num det tot", len(data_det))

# for i in range(len(data_det[data_det['isSignal']!=1])):
#     print(data_det[data_det['isSignal']!=1]["__MCDecayString__"].iloc[i])

# for i in range(len(data_gen[data_gen["isSignal"]==1])):
#     print(data_gen[data_gen["isSignal"]==1]["__MCDecayString__"].iloc[i])

# print(data["mcPDG"])
