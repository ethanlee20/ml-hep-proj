import matplotlib.pyplot as plt

from mylib.util.data import approx_num_bins, section

from mylib.plot.core.looks.leg import stats_legend


def plot_gen_det(
    data,
    var,
    q_squared_split, 
    title,
    xlabel,
    xlim=(None, None)
):
    data = section(
        data, 
        only_sig=True, 
        var=var, 
        q_squared_split=q_squared_split
    )

    if xlim != (None, None):
        data = data[(data > xlim[0]) & (data < xlim[1])]

    legends = {
        "gen":stats_legend(
            data.loc["gen"],
            "Generator"
        ),
        "det":stats_legend(
            data.loc["det"],
            "Detector (sig.)"
        )
    }

    fig, ax = plt.subplots()

    ax.hist(
        data.loc["gen"],
        label=legends["gen"],    
        bins=approx_num_bins(data.loc["gen"]),
        color="purple",
        histtype="step",
        linestyle="-",
    )

    ax.hist(
        data.loc["det"],
        label=legends["det"],    
        bins=approx_num_bins(data.loc["det"]),
        color="blue",
        histtype="step",
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    return fig, ax
