
from math import sqrt

import pandas as pd

from mylib.util.hist import (
    make_bin_edges,
    find_bin_middles,
    make_q_squared_bins,
    bin_data,
)


def calc_afb(d_cos_theta_l):
    f = d_cos_theta_l[(d_cos_theta_l > 0) & (d_cos_theta_l < 1)].count()
    b = d_cos_theta_l[(d_cos_theta_l > -1) & (d_cos_theta_l < 0)].count()
    
    afb = (f - b) / (f + b)

    afb_err = 2 * sqrt(2) * b * f / (f + b)**2

    return (afb, afb_err)


def calc_binned_afb(d_cos_theta_l, bins):
    binned = bin_data(d_cos_theta_l, bins)
    afbs = binned.apply(calc_afb, result_type='expand')
    breakpoint()
    return afbs


def calc_afb_of_q_squared(d_cos_theta_l, d_q_squared, num_points):
    bin_edges = make_bin_edges(
    	start=d_q_squared.min(), 
    	stop=d_q_squared.max(), 
    	num_bins=num_points
	)
    bins = make_q_squared_bins(d_q_squared, bin_edges)
    afbs = calc_binned_afb(d_cos_theta_l, bins)
    q_squareds = find_bin_middles(bin_edges)

    return q_squareds, afbs










