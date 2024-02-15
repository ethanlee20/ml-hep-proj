
"""Set plot limits."""

from lib.mylib.util.data import min_max_over_arrays


def set_x_lims(ax, data_gen, data_det):
    """Set the plot's x limits to contain all the data."""

    min, max = min_max_over_arrays([data_gen, data_det])
    ax.set_xlim(min - 0.05, max + 0.05)