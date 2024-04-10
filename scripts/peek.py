
import sys

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared_mix_bkg

def print_column_names(data):
    print(data.columns.values)


def print_mc_particles(data):
    max_prints = min(len(data), 10)
    for cand in range(max_prints):
        print(data["__MCDecayString__"].iloc[cand])


def print_counts(data):
    try:
        print("num gen", len(section(data, gen_det='gen')))
    except KeyError as err: print("no gen events?", err)

    try:
        print("num gen sig", len(section(data, gen_det='gen', sig_noise='sig')))
    except KeyError as err: print("no gen sig events?", err)

    try:
        print("num det sig", len(section(data, sig_noise='sig', gen_det='det')))
    except KeyError as err: print("no detector signal events?", err)

    print("num det noise", len(section(data, gen_det='det', sig_noise='noise')))

    print("num det tot", len(section(data, gen_det='det')))

    
data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-30_bdt_15i/e/mix/an')
data_bkg_all = section(data, sig_noise='noise')
data_bkg_jpsi = section(data, sig_noise='noise', q_squared_split='JPsi')
data_bkg_psi2s = section(data, sig_noise='noise', q_squared_split='Psi2S')


print(data.head())
# data_vetod = veto_q_squared_mix_bkg(data)
# data_vetod_bkg = section(data_vetod, sig_noise='noise')

# print("bkg in j/psi region below")
# print_mc_particles(data_bkg_jpsi)
# print("bkg in psi(2s) region below")
# print_mc_particles(data_bkg_psi2s)
