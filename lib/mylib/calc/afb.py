
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

    return afb


def calc_afb_err(d_cos_theta_l):
    f = d_cos_theta_l[(d_cos_theta_l > 0) & (d_cos_theta_l < 1)].count()
    b = d_cos_theta_l[(d_cos_theta_l > -1) & (d_cos_theta_l < 0)].count()
    
    n = f + b
    f_stdev = sqrt(f)
    b_stdev = sqrt(b)

    afb_stdev = 2*f*b / (f+b)**2 * sqrt((f_stdev/f)**2 + (b_stdev/b)**2)
    afb_err = afb_stdev / sqrt(n)

    return afb_err



def calc_binned_afb(d_cos_theta_l, bins):
    binned = bin_data(d_cos_theta_l, bins)
    afbs = binned.apply(calc_afb)
    errs = binned.apply(calc_afb_err)
    return afbs, errs


def calc_afb_of_q_squared(d_cos_theta_l, d_q_squared, num_points):
    bin_edges = make_bin_edges(
    	start=d_q_squared.min(), 
    	stop=d_q_squared.max(), 
    	num_bins=num_points
	)
    bins = make_q_squared_bins(d_q_squared, bin_edges)
    afbs, errs = calc_binned_afb(d_cos_theta_l, bins)
    q_squareds = find_bin_middles(bin_edges)

    return q_squareds, afbs, errs










