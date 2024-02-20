
from math import pi

from mylib.util.hist import (
    make_bin_edges,
    find_bin_middles,
    make_q_squared_bins,
    bin_data,
)


def calc_s5(d_chi, d_cos_theta_k):
    chi_f = d_chi[
        ((d_chi > 3*pi/2) & (d_chi < 2*pi)) 
        | ((d_chi > 0) & (d_chi < pi/2))
    ].count()
    chi_b = d_chi[(d_chi > pi/2) & (d_chi < 3*pi/2)].count()
    
    costheta_k_f = d_cos_theta_k[(d_cos_theta_k > 0) & (d_cos_theta_k < 1)].count()
    costheta_k_b = d_cos_theta_k[(d_cos_theta_k > -1) & (d_cos_theta_k < 0)].count()
    
    s5 = (
        4/3 * (chi_f - chi_b) * (costheta_k_f - costheta_k_b) 
        / ((chi_f + chi_b) * (costheta_k_f + costheta_k_b)) 
    )
    breakpoint()
    return s5


def calc_s5_df(df):
    d_chi = df["chi"]
    d_cos_theta_k = df["costheta_K"]
    s5 = calc_s5(d_chi, d_cos_theta_k)
    return s5


def calc_binned_s5(df, bins):
    binned = bin_data(df, bins)
    s5s = binned.apply(calc_s5_df)
    return s5s


def calc_s5_of_q_squared(df, num_points):
    d_q_squared = df["q_squared"]

    bin_edges = make_bin_edges(
        start=d_q_squared.min(), 
        stop=d_q_squared.max(), 
        num_bins=num_points
    )
    bins = make_q_squared_bins(d_q_squared, bin_edges)
    s5s = calc_binned_s5(df, bins)
    q_squareds = find_bin_middles(bin_edges)

    return q_squareds, s5s