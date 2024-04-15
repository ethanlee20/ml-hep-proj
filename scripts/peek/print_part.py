
import sys

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None

from mylib.util import open_data, section, veto_q_squared


data_dir = sys.argv[1]
veto = sys.argv[2]


def print_mc_particles(data):
    max_prints = min(len(data), 5)
    for cand in range(max_prints):
        print(data["__MCDecayString__"].iloc[cand])

    
data = open_data(data_dir)
if veto == "yes":
    data = veto_q_squared(data)

print_mc_particles(data)