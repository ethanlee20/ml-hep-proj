
import sys

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared


data_dir = sys.argv[1]
veto = sys.argv[2]


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


data = open_data(data_dir)

if veto == "yes":
    data = veto_q_squared(data)

print_counts(data)


# data_vetod_bkg = section(data_vetod, sig_noise='noise')
# data_bkg_all = section(data, sig_noise='noise')
# data_bkg_jpsi = section(data, sig_noise='noise', q_squared_split='JPsi')
# data_bkg_psi2s = section(data, sig_noise='noise', q_squared_split='Psi2S')



# print("bkg in j/psi region below")
# print_mc_particles(data_bkg_jpsi)
# print("bkg in psi(2s) region below")
# print_mc_particles(data_bkg_psi2s)
