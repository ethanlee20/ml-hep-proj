
import sys

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared_mix_bkg

def print_column_names(data):
    print(data.columns.values)


def print_mc_particles(data):
    max_prints = min(len(data), 20)
    for cand in range(max_prints):
        print(data["__MCDecayString__"].iloc[cand])


def print_counts(data):
    try:
        print("num gen", len(section(data, gen_det='gen')))
    except KeyError: print("no gen events?")

    try:
        print("num gen sig", len(section(data, gen_det='gen', sig_noise='sig')))
    except KeyError: print("no gen sig events?")

    try:
        print("num det sig", len(section(data, sig_noise='sig', gen_det='det')))
    except KeyError: print("no detector signal events?")

    print("num det noise", len(section(data, gen_det='det', sig_noise='noise')))

    print("num det tot", len(section(data, gen_det='det')))

    

data = open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-30_bdt_15i/e/charge/an')
data_vetod = veto_q_squared_mix_bkg(data)

print_counts(data)
print("vetod below")
print_counts(data_vetod)
