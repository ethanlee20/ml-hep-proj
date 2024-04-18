
import argparse

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared


parser = argparse.ArgumentParser()

parser.add_argument("data_dir")
parser.add_argument("--veto", action='store_true', help="veto out J/Psi and Psi(2S) regions of q squared")
parser.add_argument("--bg_only", action='store_true', help="only include background events")
parser.add_argument("--sig_only", action='store_true', help="only include signal events")
parser.add_argument('--gen', action='store_true', help="show generator level data")
parser.add_argument('--det', action='store_true', help="show detector level data")
parser.add_argument('--num_ex', type=int, default=5, help="number of examples to show")

parser.add_argument("--cut_var", help="variable to cut on")
parser.add_argument("--lower_bound", help="lower bound for cut", type=float)
parser.add_argument("--upper_bound", help="upper bound for cut", type=float)
parser.add_argument("--equal_to", help="equality to cut on", type=float)
parser.add_argument("--not_equal_to", help="inequality to cut on", type=float)

args = parser.parse_args()


data = open_data(args.data_dir)

if args.veto:
    data = veto_q_squared(data)

if args.bg_only:
    data = section(data, sig_noise='noise')
elif args.sig_only:
    data = section(data, sig_noise='sig')

if args.gen:
    data = section(data, gen_det='gen')
elif args.det:
    data = section(data, gen_det='det')

if args.cut_var:
    assert (args.lower_bound is not None) | (args.upper_bound is not None) | (args.equal_to is not None) | (args.not_equal_to is not None), "must specify cut details"
    if (args.lower_bound is not None) & (args.upper_bound is not None):
        data = data[(data[args.cut_var] >= args.lower_bound) & (data[args.cut_var] <= args.upperbound)]
    elif args.lower_bound is not None:
        data = data[data[args.cut_var] >= args.lower_bound]
    elif args.upper_bound is not None:
        data = data[data[args.cut_var] <= args.upper_bound]
    elif args.equal_to is not None:
        data = data[data[args.cut_var] == args.equal_to]
    elif args.not_equal_to is not None:
        data = data[data[args.cut_var] != args.not_equal_to]


print(data.head(args.num_ex))