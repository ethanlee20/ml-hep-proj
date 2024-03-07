
from mylib.util.data import find_num_events, split_by_q_squared, only_signal

from mylib.plot.core.hist.hist_2d import plot_hist_2d_side_by_side, add_color_bar


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