
import argparse

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared


parser = argparse.ArgumentParser()
parser.add_argument("data_dir")
parser.add_argument("--veto", action='store_true')
parser.add_argument("--bg_only", action='store_true')
parser.add_argument("--sig_only", action='store_true')
parser.add_argument('--gen', action='store_true')
parser.add_argument('--det', action='store_true')
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


print(data.head())