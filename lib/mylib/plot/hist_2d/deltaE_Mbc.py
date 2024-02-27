
import matplotlib.pyplot as plt
from mylib.plot.core.util.save import save
from mylib.plot.hist_2d.base import make_ax_labels

from mylib.plot.hist_2d.hist_2d import add_color_bar, plot_hist_2d_side_by_side


def hist2d_deltaE_mbc(data, out_dir):
    fig, axs, norm = plot_hist_2d_side_by_side(
        xs=[
            data[data["isSignal"]==1].loc["det"]["Mbc"],
            data[data["isSignal"]==0].loc["det"]["Mbc"],
        ],
        ys=[
            data[data["isSignal"]==1].loc["det"]["deltaE"],
            data[data["isSignal"]==0].loc["det"]["deltaE"],
        ],
        num_bins=50,
    )

    add_color_bar(axs, norm)

    save("mbc_deltaE", q_squared_split="all", out_dir=out_dir)

