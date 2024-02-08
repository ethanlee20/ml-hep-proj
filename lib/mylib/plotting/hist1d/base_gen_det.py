from mylib.utilities.data import split_by_q_squared, only_signal

from mylib.plotting.core.hist.hist import approx_num_bins

from mylib.plotting.core.augments.legend import stats_legend


def plot_gen_det(
    data,
    var,
    q_squared_split, 
    title,
    xlabel,
):

    data = split_by_q_squared(
        only_signal(data)
    )[q_squared_split][var]
    
    num_bins = approx_num_bins(
        data.loc["det"]
    )

    legends = {
        "gen":stats_legend(
            data.loc["gen"]
            "Generator"
        ),
        "det":stats_legend(
            data.loc["det"],
            "Detector"
        )
    }

    fig, ax = plt.subplots()

    ax.hist(
        data.loc["gen"],
        label=legends["gen"],    
        bins=num_bins,
        color="purple",
        histtype="step",
        linestyle="-",
    )

    ax.hist(
        data.loc["det"],
        label=legends["det"],    
        bins=num_bins,
        color="blue",
        histtype="step",
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    return fig, ax
