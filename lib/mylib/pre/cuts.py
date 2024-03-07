
import pathlib as pl

import numpy as np
import pandas as pd

from mylib.calc.phys import calc_dif_inv_mass_k_pi_and_kst
from mylib.util.data import count_events


def cut_on_kst_inv_mass(df):
    kst_full_width = 0.05
    in_cut = (
        calc_dif_inv_mass_k_pi_and_kst(df).abs()
        <= 1.5 * kst_full_width
    )
    cut_df = df[in_cut].copy() 
    return cut_df


def cut_on_mbc(df):
    mbc_low_bound = 5.27
    in_cut = df["Mbc"] > mbc_low_bound
    cut_df = df[in_cut].copy()
    return cut_df


def cut_on_deltaE(df):
    in_cut = abs(df["deltaE"]) <= 0.05
    cut_df = df[in_cut].copy()
    return cut_df


def apply_all_cuts_with_summary(df):
    cut_df1 = cut_on_kst_inv_mass(df)
    cut_df2 = cut_on_mbc(cut_df1)
    cut_df3 = cut_on_deltaE(cut_df2)

    n_cut0_sig = count_events(df[df["isSignal"]==1])
    n_cut1_sig = count_events(cut_df1[cut_df1["isSignal"]==1])
    n_cut2_sig = count_events(cut_df2[cut_df2["isSignal"]==1])
    n_cut3_sig = count_events(cut_df3[cut_df3["isSignal"]==1])

    n_cut0_mis = count_events(df[df["isSignal"]==0])
    n_cut1_mis = count_events(cut_df1[cut_df1["isSignal"]==0])
    n_cut2_mis = count_events(cut_df2[cut_df2["isSignal"]==0])
    n_cut3_mis = count_events(cut_df3[cut_df3["isSignal"]==0])

    n_cut0_tot = count_events(df)
    n_cut1_tot = count_events(cut_df1)
    n_cut2_tot = count_events(cut_df2)
    n_cut3_tot = count_events(cut_df3)

    n_sig = np.array([n_cut0_sig, n_cut1_sig, n_cut2_sig, n_cut3_sig])
    n_mis = np.array([n_cut0_mis, n_cut1_mis, n_cut2_mis, n_cut3_mis])
    n_tot = np.array([n_cut0_tot, n_cut1_tot, n_cut2_tot, n_cut3_tot])

    summ = pd.DataFrame({"sig":n_sig, "mis":n_mis, "tot":n_tot})

    return cut_df3, summ


def make_total_count_summary(dir):
    dir = pl.Path(dir)
    paths = dir.glob('*summ.csv')
    summs = [pd.read_csv(path) for path in paths]
    total = sum(summs)
    return total
