
import matplotlib.pyplot as plt


def generate_plot_file_name(plot_name, q_squared_split):
    return f"q2{q_squared_split}_{plot_name}.png"


def save_fig_and_clear(out_dir_path, plot_name):
    file_name = generate_plot_file_name(plot_name, q_squared_split)
    plt.savefig(out_dir_path.joinpath(file_name), bbox_inches="tight")
    plt.close()
