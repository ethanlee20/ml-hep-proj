
from myargparser import parser
parser.add_argument('--num_ex', type=int, default=5, help="number of examples to show")

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared


args = parser.parse_args()

data = open_data(args.data_path)

if args.veto_q2:
    data = veto_q_squared(data)

if args.noise_only:
    data = section(data, sig_noise='noise')
elif args.sig_only:
    data = section(data, sig_noise='sig')

if args.gen_only:
    data = section(data, gen_det='gen')
elif args.det_only:
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