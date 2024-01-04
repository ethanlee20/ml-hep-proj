import os
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))

import physics
import plotting


# Cuts

def kst_inv_mass_cut(df_data, plot_dir):
    def calculate_inv_mass_k_pi():
        df_k_4mom = df_data[["K_m_E", "K_m_px", "K_m_py", "K_m_pz"]]
        df_pi_4mom = df_data[["pi_p_E", "pi_p_px", "pi_p_py", "pi_p_pz"]]
        df_inv_mass_k_pi = np.sqrt(
            physics.invariant_mass_squared_two_particles(df_k_4mom, df_pi_4mom)
        )
        return df_inv_mass_k_pi

    def calculate_difference_inv_mass_k_pi_inv_mass_kst():
        inv_mass_kst = 0.892
        df_inv_mass_k_pi = calculate_inv_mass_k_pi()
        df_data["inv_mass_k_pi - inv_mass_kst"] = df_inv_mass_k_pi - inv_mass_kst

    calculate_difference_inv_mass_k_pi_inv_mass_kst()

    def cut_on_inv_mass_k_pi():
        kst_full_width = 0.05
        cut = df_data["inv_mass_k_pi - inv_mass_kst"].abs() <= 1.5 * kst_full_width
        return df_data[cut]

    df_cut_data = cut_on_inv_mass_k_pi()

    def plot_before_cut():
        plotting.setup_mpl_params_save()
        title = r"$M_{K^-\pi^+} - M_{K^*(892)}$, before cut on width"
        xlabel = r"[GeV]"
        plotting.plot_signal_and_misrecon(df_data, "inv_mass_k_pi - inv_mass_kst", "isSignal", title, xlabel)
        plt.savefig(os.path.join(plot_dir, "inv_mass_cut_before.png"), bbox_inches="tight")
        plt.clf()    

    plot_before_cut()
    
    def plot_after_cut():
        title = r"$M_{K^-\pi^+} - M_{K^*(892)}$, after cut on width"
        xlabel = r"[GeV]"
        plotting.plot_signal_and_misrecon(df_cut_data, "inv_mass_k_pi - inv_mass_kst", "isSignal", title, xlabel)    
        plt.savefig(os.path.join(plot_dir, "inv_mass_cut_after.png"), bbox_inches="tight")
        plt.clf()
        
    plot_after_cut()
    
    return df_cut_data

    
def mbc_cut(df_data, plot_dir):

    mbc_low_bound = 5.27
    cut = df_data["Mbc"] > mbc_low_bound
    df_cut_data = df_data[cut]

    def plot_before_cut():
        plotting.setup_mpl_params_save()
        title = r"$\Delta E$ before cut on $M_{bc}$"
        xlabel = r"[GeV]"
        plotting.plot_signal_and_misrecon(df_data, "deltaE", "isSignal", title, xlabel)
        plt.savefig(os.path.join(plot_dir, "mbc_cut_before.png"), bbox_inches="tight")
        plt.clf()

    plot_before_cut()
    
    def plot_after_cut():
        title = r"$\Delta E$ after cut on $M_{bc}$"
        xlabel = r"[GeV]"       
        plotting.plot_signal_and_misrecon(df_cut_data, "deltaE", "isSignal",  title, xlabel)
        plt.savefig(os.path.join(plot_dir, "mbc_cut_after.png"), bbox_inches="tight")
        plt.clf()

    plot_after_cut()

    return df_cut_data


def deltaE_cut(df_data, plot_dir):

    cut = abs(df_data["deltaE"]) <= 0.05
    df_cut_data = df_data[cut]

    def plot_before_cut():
        plotting.setup_mpl_params_save()
        title = r"$M_{bc}$ before cut on $\Delta E$"
        xlabel = r"[GeV]"
        plotting.plot_signal_and_misrecon(df_data, "Mbc", "isSignal", title, xlabel)
        plt.savefig(os.path.join(plot_dir, "deltaE_cut_before.png"), bbox_inches="tight")
        plt.clf()

    plot_before_cut()
    
    def plot_after_cut():
        title = r"$M_{bc}$ after cut on $\Delta E$"
        xlabel = r"[GeV]"       
        plotting.plot_signal_and_misrecon(df_cut_data, "Mbc", "isSignal",  title, xlabel)
        plt.savefig(os.path.join(plot_dir, "deltaE_cut_after.png"), bbox_inches="tight")
        plt.clf()

    plot_after_cut()

    return df_cut_data


def apply_all_cuts(df_data, plot_dir):
    df_cut1_data = kst_inv_mass_cut(df_data, plot_dir)
    df_cut2_data = mbc_cut(df_cut1_data,  plot_dir)
    df_cut3_data = deltaE_cut(df_cut2_data, plot_dir)
    return df_cut3_data
