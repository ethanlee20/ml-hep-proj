
import argparse
import pathlib as pl

import matplotlib.pyplot as plt

from mylib.plot import (
    setup_mpl_params_save,
    stats_legend,
    plot_sm_np_comp
)
from mylib.util import open_data


sm_data = open_data(input_path)
np_data = 

if args.plot_name == "deltaE_mbc_gen_det":
    fig, ax = plot_gen_det(
        data=data,
        var="deltaE",
        q_squared_split="all",
        title=r"$\Delta E $"
    )
    






