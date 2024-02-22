import numpy as np

from mylib.calc.phys import invariant_mass_squared_two_particles


def calculate_inv_mass_k_pi(df):
    df_k_4mom = df[
        ["K_p_E", "K_p_px", "K_p_py", "K_p_pz"]
    ]
    df_pi_4mom = df[
        ["pi_m_E", "pi_m_px", "pi_m_py", "pi_m_pz"]
    ]
    df_inv_mass_k_pi = np.sqrt(
        invariant_mass_squared_two_particles(
            df_k_4mom, df_pi_4mom
        )
    )
    return df_inv_mass_k_pi


def calc_dif_inv_mass_k_pi_and_kst(df):
    inv_mass_kst = 0.892
    df_inv_mass_k_pi = calculate_inv_mass_k_pi(df)
    dif = df_inv_mass_k_pi - inv_mass_kst
    return dif


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


def apply_all_cuts(df):
    cut_df1 = cut_on_kst_inv_mass(df)
    cut_df2 = cut_on_mbc(cut_df1)
    cut_df3 = cut_on_deltaE(cut_df2)
    return cut_df3
