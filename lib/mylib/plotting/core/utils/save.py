
import functools
import matplotlib.pyplot as plt


def plot_file_name(plot_name, q_squared_split):
    return f"q2{q_squared_split}_{plot_name}.png"


def save_fig_and_clear(file_name, out_dir):
    plt.savefig(out_dir.joinpath(file_name), bbox_inches="tight")
    plt.close()


def save(plot_name, q_squared_split, out_dir):
    file_name = plot_file_name(plot_name, q_squared_split)
    save_fig_and_clear(file_name, out_dir)
