import os
import sys

import pandas as pd
import numpy as np

sys.path.append(
    os.path.join(os.path.dirname(__file__), "../")
)

import eff_and_res
import test_df


def test_generate_bin_edges():
    bin_edges = eff_and_res.generate_bin_edges(
        start=1.2,
        stop=2.4,
        num_of_bins=4,
    )
    np.testing.assert_allclose(bin_edges, np.array([1.2,1.5,1.8,2.1,2.4]))


def test_find_bin_middles():
    bin_edges = eff_and_res.generate_bin_edges(
        start=1.2,
        stop=2.4,
        num_of_bins=4,
    )

    bin_middles = eff_and_res.find_bin_middles(bin_edges)

    np.testing.assert_allclose(bin_middles, np.array([1.35, 1.65, 1.95, 2.25]))


def test_find_bin_counts():

    bin_edges = eff_and_res.generate_bin_edges(
        start=0,
        stop=10,
        num_of_bins=4
    )
    bin_counts = eff_and_res.find_bin_counts(
        data=test_df.test_df_c,
        binning_variable="d",
        bin_edges=bin_edges
    )
    
    print(bin_counts)

#    should be the following, but can't get index to work:
#
#    target_bin_index = CategoricalIndex(
#        [(-0.001, 2.5], (2.5, 5.0], (5.0, 7.5], (7.5, 10.0]],
#        categories=[(-0.001, 2.5], (2.5, 5.0], (5.0, 7.5], (7.5, 10.0]], 
#        ordered=True, 
#        name='d', 
#        dtype='category'
#    )
#    
#    target_bin_counts = pd.Series([5, 3, 2,0], index=target_bin_index)
#    
#    pd.testing.assert_series_equal(bin_counts, target_bin_counts)


def test_calculate_efficiency():
    bin_edges = eff_and_res.generate_bin_edges(
        start=0,
        stop=10,
        num_of_bins=4
    )

    eff = eff_and_res.calculate_efficiency(test_df.test_df_c, test_df.test_df_d, "d", bin_edges)

    np.testing.assert_allclose(eff, np.array([1, 0.75, np.inf, 0]))
