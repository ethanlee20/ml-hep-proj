
import argparse

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared


parser = argparse.ArgumentParser()
parser.add_argument("data_dir")
parser.add_argument("--veto", action='store_true', help="veto out J/Psi and Psi(2S) regions of q squared")
parser.add_argument("--cut_var", help="variable to cut on")
parser.add_argument("--lower_bound", help="lower bound to cut on (in terms of specified variable)")
parser.add_argument("--upper_bound", help="upper bound to cut on (in terms of specified variable)")
parser.add_argument("--equal_to", help="equality to cut on (in terms of specified variable)")
args = parser.parse_args()



data = open_data(args.data_dir)

if args.veto:
    data = veto_q_squared(data)

if args.cut_var:
    assert (args.lower_bound is not None) | (args.upper_bound is not None) | (args.equal_to is not None), "must specify cut details"
    if (args.lower_bound is not None) & (args.upper_bound is not None):
        data = data[(data[args.cut_var] >= args.lower_bound) & (data[args.cut_var] <= args.upperbound)]
    elif args.lower_bound is not None:
        data = data[data[args.cut_var] >= args.lower_bound]
    elif args.upper_bound is not None:
        data = data[data[args.cut_var] <= args.upper_bound]
    elif args.equal_to is not None:
        data = data[data[args.cut_var] == args.equal_to]


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


print_counts(data)


# data_vetod_bkg = section(data_vetod, sig_noise='noise')
# data_bkg_all = section(data, sig_noise='noise')
# data_bkg_jpsi = section(data, sig_noise='noise', q_squared_split='JPsi')
# data_bkg_psi2s = section(data, sig_noise='noise', q_squared_split='Psi2S')



# print("bkg in j/psi region below")
# print_mc_particles(data_bkg_jpsi)
# print("bkg in psi(2s) region below")
# print_mc_particles(data_bkg_psi2s)
