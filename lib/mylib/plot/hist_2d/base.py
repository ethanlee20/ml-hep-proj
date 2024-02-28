
from mylib.util.data import find_num_events, split_by_q_squared, only_signal

from mylib.plot.core.hist.hist_2d import plot_hist_2d_side_by_side, add_color_bar

from mylib.plotting.core.augments.labels import Labels, set_plot_labels


def make_titles(num_gen_events, num_det_events):
    titles = {
        "gen": "Generator" + r" \small{Count: " + f"{num_gen_events}" + "}",
        "det": "Detector" + r" \small{Count: " + f"{num_det_events}" + "}"    
    }
    return titles


def make_ax_labels(num_gen_events, num_det_events):
    titles = make_titles(num_gen_events, num_det_events)
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
    data = split_by_q_squared(data)[q_squared_split]

    fig, axs, norm = plot_hist_2d_side_by_side(
        xs=[
            data.loc["gen"][var_x],
            data.loc["det"][var_x],
        ],
        ys=[
            data.loc["gen"][var_y],
            data.loc["det"][var_y],
        ],
        num_bins=50,
    )

    add_color_bar(axs, norm)

    ax_labels = make_ax_labels(
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