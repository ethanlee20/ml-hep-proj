
import matplotlib.pyplot as plt

from mylib.utilities.data import find_num_events

from mylib.calculating.efficiency import calculate_efficiency


def make_legend(data, q_squared_split, var):
    data = only_signal(data)
    data = split_by_q_squared(data)[q_squared_split]
    data = data[var]

    num_events = {
        "gen":find_num_events(data.loc["gen"]),
        "det":find_num_events(data.loc["det"])
    }

    legend = {
        "calc": r"\textbf{Calculated}" + f"\nDetector (signal): {num_events['det']}\nGenerator: {num_events['gen']}",
        "mc": r"\textbf{MC Truth}"
    }

    return legend


def plot_efficiency(
    data,
    var,
    q_squared_split,
    num_points,
    title,
    xlabel,
    **kwargs,
):

    efficiency, bin_middles, errors = calculate_efficiency(data, var, num_points, q_squared_split)
    efficiency_mc, bin_middles_mc, errors_mc = calculate_efficiency(data, var, num_points, q_squared_split, mc=True)

    fig, ax = plt.subplots()

    legend = make_legend(data, q_squared_split, var)

    ax.scatter(
        bin_middles, 
        efficiency,
        label=legend["calc"],
        color="red",
        alpha=0.5,
        **kwargs,
    )
    ax.errorbar(
        bin_middles,
        efficiency,
        yerr=errors,
        fmt="none",
        capsize=5,
        color="black",
        alpha=0.5,
        **kwargs,
    )

    ax.scatter(
        bin_middles_mc,
        efficiency_mc,
        label=legend["mc"],
        color="blue",
        alpha=0.5,
        **kwargs,
    )
    ax.errorbar(
        bin_middles_mc,
        efficiency_mc,
        yerr=errors_mc,
        fmt="none",
        capsize=5,
        color="orange",
        alpha=0.5,
        **kwargs,
    )

    ax.legend()
    ax.set_xlim(data[variable].min() - 0.05, data[variable].max() + 0.05)
    ax.set_ymargin(0.25)
    ax.set_ylim(bottom=0, top=0.5)
    ax.set_ylabel(r"$\varepsilon$", rotation=0, labelpad=20)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    return fig, ax


