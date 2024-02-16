
"""Plot labeling stuff."""


import matplotlib.pyplot as plt
import numpy as np


class Labels:
    def __init__(self, title=None, xlabel=None, ylabel=None):
        self.title = title
        self.x = xlabel
        self.y = ylabel


def set_ax_labels(ax, labels):
    ax.set_title(labels.title)
    ax.set_xlabel(labels.x)
    ax.set_ylabel(labels.y)


def set_fig_labels(fig, labels):
    fig.suptitle(labels.title)
    fig.supxlabel(labels.x)
    fig.supylabel(labels.y)


def set_plot_labels(
    fig, 
    axs: list, 
    ax_labels: list,
    fig_labels,
):
    for ax, labels in zip(axs, ax_labels):
        set_ax_labels(ax, labels)
        
    set_fig_labels(fig, fig_labels)




    


