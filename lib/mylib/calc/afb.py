
from math import sqrt

import pandas as pd

from mylib.util.hist import (
    find_bin_middles,
    bin_data,
)


def calc_afb(ell):
    def calc(df):
        if ell == 'mu':
            d_cos_theta_l = df['costheta_mu']
        elif ell == 'e':
            d_cos_theta_l = df['costheta_e']

        f = d_cos_theta_l[(d_cos_theta_l > 0) & (d_cos_theta_l < 1)].count()
        b = d_cos_theta_l[(d_cos_theta_l > -1) & (d_cos_theta_l < 0)].count()
        
        afb = (f - b) / (f + b)

        return afb
    return calc

def calc_afb_err(ell):
    def calc(df):
        if ell == 'mu':
            d_cos_theta_l = df['costheta_mu']
        elif ell == 'e':
            d_cos_theta_l = df['costheta_e']


        f = d_cos_theta_l[(d_cos_theta_l > 0) & (d_cos_theta_l < 1)].count()
        b = d_cos_theta_l[(d_cos_theta_l > -1) & (d_cos_theta_l < 0)].count()
        
        n = f + b
        f_stdev = sqrt(f)
        b_stdev = sqrt(b)

        afb_stdev = 2*f*b / (f+b)**2 * sqrt((f_stdev/f)**2 + (b_stdev/b)**2)
        afb_err = afb_stdev #/ sqrt(n)

        return afb_err
    return calc


def calc_afb_of_q_squared(df, ell, num_points):
    binned, edges = bin_data(df, 'q_squared', num_points, ret_edges=True)
    
    afbs = binned.apply(calc_afb(ell))
    errs = binned.apply(calc_afb_err(ell))
    q_squareds = find_bin_middles(edges)

    return q_squareds, afbs, errs










