
import matplotlib.pyplot as plt
from mylib.plot.core.util.save import save

from mylib.plot.core.hist_2d.hist_2d import add_color_bar, plot_hist_2d_side_by_side
from mylib.util.data import count_events


def hist2d_deltaE_mbc(data, out_dir, sig_only=False):

    n_bins = 50

    if sig_only:
        sig = data[data["isSignal"]==1].loc["det"]
        breakpoint()
        plt.hist2d(sig["Mbc"].values, sig["deltaE"].values, bins=n_bins, cmap='hot')
        plt.colorbar()
        plt.title(r"Signal \small" + f"(count: {count_events(sig)})")
        plt.ylabel(r"$\Delta E$ [GeV]")
        plt.xlabel(r"$M_{bc}$ [GeV]")
        save("mbc_deltaE_onlySig", q_squared_split="all", out_dir=out_dir)
        return
    
    sig = data[data["isSignal"]==1].loc["det"]
    mis = data[data["isSignal"]==0].loc["det"]

    fig, axs, norm = plot_hist_2d_side_by_side(
        xs=[
            sig["Mbc"],
            mis["Mbc"],
        ],
        ys=[
            sig["deltaE"],
            mis["deltaE"],
        ],
        num_bins=n_bins,
    )

    add_color_bar(axs, norm)

    axs[0].set_title(r"Signal \small" + f"(count: {count_events(sig)})")
    axs[1].set_title(r"Misrecon. \small" + f"(count: {count_events(mis)})")
    axs[0].set_ylabel(r"$\Delta E$ [GeV]")
    fig.supxlabel(r"$M_{bc}$ [GeV]")

    save("mbc_deltaE", q_squared_split="all", out_dir=out_dir)

