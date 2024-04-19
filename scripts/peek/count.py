
from myargparser import parser

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared



args = parser.parse_args()

data = open_data(args.data_path)

if args.veto_q2:
    data = veto_q_squared(data)

# if args.cut_var:
#     assert (args.lower_bound is not None) | (args.upper_bound is not None) | (args.equal_to is not None) | (args.not_equal_to is not None), "must specify cut details"
#     if (args.lower_bound is not None) & (args.upper_bound is not None):
#         data = data[(data[args.cut_var] >= args.lower_bound) & (data[args.cut_var] <= args.upperbound)]
#     elif args.lower_bound is not None:
#         data = data[data[args.cut_var] >= args.lower_bound]
#     elif args.upper_bound is not None:
#         data = data[data[args.cut_var] <= args.upper_bound]
#     elif args.equal_to is not None:
#         data = data[data[args.cut_var] == args.equal_to]
#     elif args.not_equal_to is not None:
#         data = data[data[args.cut_var] != args.not_equal_to]


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
