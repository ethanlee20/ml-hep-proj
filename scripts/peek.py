import sys
import pathlib as pl

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util.util import open_data

#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/mu_re_00030_job386260858_00_cut_an.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00000_job386260828_00.root'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00001_job386260829_00.root'
# data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00003_job388070872_00_cut_an.pkl')


def print_column_names(data):
    print(data.columns.values)


def print_mc_particles(data):
    max_prints = min(len(data), 20)
    for cand in range(max_prints):
        print(data["__MCDecayString__"].iloc[cand])


def sig(data):
    isSignal = (data["isSignal"]==1) & (data["KST0_isSignal"]==1) & (data["K_p_isSignal"]==1) & (data["pi_m_isSignal"]==1) & (data["e_p_isSignal"]==1) & (data["e_m_isSignal"]==1)
    return data[isSignal]


def bkg(data):
    isBkg = (data["isSignal"]!=1) | (data["KST0_isSignal"]!=1) | (data["K_p_isSignal"]!=1) | (data["pi_m_isSignal"]!=1) | (data["e_p_isSignal"]!=1) | (data["e_m_isSignal"]!=1)
    return data[isBkg]


def check_strange(data):
    isStrange = (data["isSignal"]==1) & ((data["isSignalAcceptBremsPhotons"]!=1) | (data["KST0_isSignalAcceptBremsPhotons"]!=1) | (data["K_p_isSignalAcceptBremsPhotons"]!=1) | (data["pi_m_isSignalAcceptBremsPhotons"]!=1) | (data["e_p_isSignalAcceptBremsPhotons"]!=1) | (data["e_m_isSignalAcceptBremsPhotons"]!=1))
    print(data[isStrange].head())
    return data[isStrange]


def print_counts(data):
    try:
        print("num gen", len(data.loc["gen"]))
    except KeyError: print("no gen events?")

    try:
        print("num gen sig", len(sig(data).loc["gen"]))
    except KeyError: print("no gen sig events?")

    try:
        print("num det sig", len(sig(data).loc["det"]))
    except KeyError: print("no detector signal events?")

    print("num det bkg", len(bkg(data).loc["det"]))

    print("num det tot", len(data.loc["det"]))

    print("Num strange:", len(check_strange(data)))
    




# data = open_data([
#     "/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/gen_mix_e_bdt1/sub00",
#     "/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/gen_mix_e_bdt2/sub00",
#     "/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/gen_mix_e_bdt3/sub00",
#     "/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/gen_mix_e_bdt4/sub00",
#     "/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/gen_mix_e_bdt5/sub00",
# ])
data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-25_pdgTest/sig_e_bdt_checkPDG_brems/sub00')
# print(data.head())
# print_column_names(data)
print_counts(data)
# print_mc_particles(sig(data).loc["det"])
# print_mc_particles(bkg(data).loc["det"])
# print_mc_particles(sig(data).loc["gen"])



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
