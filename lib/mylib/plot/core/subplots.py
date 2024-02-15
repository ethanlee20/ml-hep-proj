
import matplotlib.pyplot as plt


def subplots_side_by_side():
    fig, axs = plt.subplots(
        ncols=2,
        layout="constrained",
        sharey=True,
    )
    return fig, axs
