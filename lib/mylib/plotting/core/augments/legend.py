import numpy as np

from mylib.utilities.data import find_num_events


def calculate_stats(ar):
    mean = np.mean(ar)
    count = find_num_events(ar)
    rms = np.std(ar)
    stats = {
        "mean": mean,
        "count": count,
        "rms": rms,
    }
    return stats


def stats_legend(
    dat_ser,
    descrp="",
    show_mean=True,
    show_count=True,
    show_rms=True,
):
    stats = calculate_stats(dat_ser)

    leg = ""
    if descrp != "":
        leg += r"\textbf{" + f"{descrp}" + "}"
    if show_mean:
        leg += f"\nMean: {stats['mean']:.2G}"
    if show_count:
        leg += f"\nCount: {stats['count']}"
    if show_rms:
        leg += f"\nRMS: {stats['rms']:.2G}"

    return leg
