
from mylib.utilities.data import find_num_events, split_by_q_squared, only_signal

from mylib.plotting.core.hist.hist_2d import plot_hist_2d_side_by_side

from mylib.plotting.core.augments.labels import Labels, set_plot_labels


def titles(num_gen_events, num_det_events):
    titles = {
        "gen": "Generator" + r"\footnotesize{Count: " + f"{num_gen_events}" + "}",
        "det": "Detector" + r"\footnotesize{Count: " + f"{num_det_events}" + "}"    
    }
    return titles


def ax_labels(num_gen_events, num_det_events):
    titles = titles(num_gen_events, num_det_events)
    ax_labels = [
        Labels(title=titles["gen"]), 
        Labels(title=titles["det"])
    ]
    return ax_labels


def plot_hist_2d(
    data,
    var_x,
    var_y,
    q_squared_split,
    xlabel,
    ylabel,
):
    data = only_signal(data)
    data = split_by_q_squared(data)

    fig, axs, norm = plot_hist_2d_side_by_side(
        xs=[
            data[q_squared_split].loc["gen"][var_x],
            data[q_squared_split].loc["det"][var_x],
        ],
        ys=[
            data[q_squared_split].loc["gen"][var_y],
            data[q_squared_split].loc["det"][var_y],
        ],
        num_bins=50,
    )

    add_color_bar(axs, norm)

    ax_labels = ax_labels(
        find_num_events(data.loc["gen"]), 
        find_num_events(data.loc["det"])
    )
    
    fig_labels = Labels(xlabel=xlabel, ylabel=ylabel)
    
    set_plot_labels(
        fig,
        axs,
        ax_labels,
        fig_labels
    )

    return fig, axs