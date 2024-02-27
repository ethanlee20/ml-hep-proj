
from math import pi, sqrt
import numpy as np

from mylib.util.hist import (
    make_bin_edges,
    find_bin_middles,
    make_q_squared_bins,
    bin_data,
)

from mylib.util.data import count_events


def calc_s5(df):
    costheta_k = df["costheta_K"]
    chi = df["chi"]
    
    f = count_events(df[
        (((costheta_k > 0) & (costheta_k < 1)) & ((chi > 0) & (chi < pi/2)))
        | (((costheta_k > 0) & (costheta_k < 1)) & ((chi > 3*pi/2) & (chi < 2*pi)))
        | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > pi/2) & (chi < 3*pi/2)))
    ])

    b = count_events(df[
        (((costheta_k > 0) & (costheta_k < 1)) & ((chi > pi/2) & (chi < 3*pi/2)))
        | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > 0) & (chi < pi/2)))
        | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > 3*pi/2) & (chi < 2*pi)))
    ])

    try: 
        s5 = 4/3 * (f - b) / (f + b)
    except ZeroDivisionError:
        print("division by 0, returning nan")
        s5 = np.nan
    
    return s5


def calc_s5_err(df):
    costheta_k = df["costheta_K"]
    chi = df["chi"]
    
    f = count_events(df[
        (((costheta_k > 0) & (costheta_k < 1)) & ((chi > 0) & (chi < pi/2)))
        | (((costheta_k > 0) & (costheta_k < 1)) & ((chi > 3*pi/2) & (chi < 2*pi)))
        | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > pi/2) & (chi < 3*pi/2)))
    ])

    b = count_events(df[
        (((costheta_k > 0) & (costheta_k < 1)) & ((chi > pi/2) & (chi < 3*pi/2)))
        | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > 0) & (chi < pi/2)))
        | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > 3*pi/2) & (chi < 2*pi)))
    ])

    f_stdev = sqrt(f)
    b_stdev = sqrt(b)

    n = f + b

    try: 
        stdev = 4/3 * 2*f*b / (f+b)**2 * sqrt((f_stdev/f)**2 + (b_stdev/b)**2)
        err = stdev# / sqrt(n)

    except ZeroDivisionError:
        print("division by 0, returning nan")
        err = np.nan
    
    return err


def calc_binned_s5(df, bins):
    binned = bin_data(df, bins)
    s5s = binned.apply(calc_s5)
    errs = binned.apply(calc_s5_err)
    return s5s, errs


def calc_s5_of_q_squared(df, num_points):
    d_q_squared = df["q_squared"]

    bin_edges = make_bin_edges(
        start=d_q_squared.min(), 
        stop=d_q_squared.max(), 
        num_bins=num_points
    )
    bins = make_q_squared_bins(d_q_squared, bin_edges)
    s5s, errs = calc_binned_s5(df, bins)
    q_squareds = find_bin_middles(bin_edges)

    return q_squareds, s5s, errs

