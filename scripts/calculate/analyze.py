import sys
import pathlib

import pandas as pd

import mylib


# Setup

data_dir = pathlib.Path(sys.argv[1])

input_file_names = [pathlib.Path(file_name) for file_name in sys.argv[2:]]
input_file_paths = [data_dir.joinpath(file_name) for file_name in input_file_names]

output_file_names = [file_name.stem + '_analyzed' + file_name.suffix for file_name in input_file_names]
output_file_paths = [data_dir.joinpath(file_name) for file_name in output_file_names]


def run_analysis(input_file_path, output_file_path):

    # setup
    df_B0 = pd.read_pickle(input_file_path)
    df_B_4mom = mylib.four_momemtum_dataframe(df_B0[["E", "px", "py", "pz"]])
    df_B_4mom_mc = mylib.four_momemtum_dataframe(df_B0[["mcE", "mcPX", "mcPY", "mcPZ"]])
    df_mu_p_4mom = mylib.four_momemtum_dataframe(df_B0[["mu_p_E", "mu_p_px", "mu_p_py", "mu_p_pz"]])
    df_mu_p_4mom_mc = mylib.four_momemtum_dataframe(df_B0[["mu_p_mcE", "mu_p_mcPX", "mu_p_mcPY", "mu_p_mcPZ"]])
    df_mu_m_4mom = mylib.four_momemtum_dataframe(df_B0[["mu_m_E", "mu_m_px", "mu_m_py", "mu_m_pz"]])
    df_mu_m_4mom_mc = mylib.four_momemtum_dataframe(df_B0[["mu_m_mcE", "mu_m_mcPX", "mu_m_mcPY", "mu_m_mcPZ"]])
    df_K_4mom = mylib.four_momemtum_dataframe(df_B0[["K_m_E", "K_m_px", "K_m_py", "K_m_pz"]])
    df_K_4mom_mc = mylib.four_momemtum_dataframe(df_B0[["K_m_mcE", "K_m_mcPX", "K_m_mcPY", "K_m_mcPZ"]])
    df_KST_4mom = mylib.four_momemtum_dataframe(df_B0[["KST0_E", "KST0_px", "KST0_py", "KST0_pz"]])
    df_KST_4mom_mc = mylib.four_momemtum_dataframe(df_B0[["KST0_mcE", "KST0_mcPX", "KST0_mcPY", "KST0_mcPZ"]])

    # solve
    df_B0["q_squared"] = mylib.invariant_mass_squared_two_particles(df_mu_p_4mom, df_mu_m_4mom)
    df_B0["q_squared_mc"] = mylib.invariant_mass_squared_two_particles(df_mu_p_4mom_mc, df_mu_m_4mom_mc)
    df_B0["costheta_mu"] = mylib.find_costheta_mu(
        df_mu_p_4mom, df_mu_m_4mom, df_B_4mom
    )
    df_B0["costheta_mu_mc"] = mylib.find_costheta_mu(
        df_mu_p_4mom_mc, df_mu_m_4mom_mc, df_B_4mom_mc
    )
    df_B0["costheta_K"] = mylib.find_costheta_K(df_K_4mom, df_KST_4mom, df_B_4mom)
    df_B0["costheta_K_mc"] = mylib.find_costheta_K(df_K_4mom_mc, df_KST_4mom_mc, df_B_4mom_mc)
    df_B0["coschi"] = mylib.find_coschi(
        df_B_4mom, df_K_4mom, df_KST_4mom, df_mu_p_4mom, df_mu_m_4mom
    )
    df_B0["coschi_mc"] = mylib.find_coschi(
        df_B_4mom_mc, df_K_4mom_mc, df_KST_4mom_mc, df_mu_p_4mom_mc, df_mu_m_4mom_mc
    )
    df_B0["chi"] = mylib.find_chi(
        df_B_4mom,
        df_K_4mom,
        df_KST_4mom,
        df_mu_p_4mom,
        df_mu_m_4mom,
    )
    df_B0["chi_mc"] = mylib.find_chi(
        df_B_4mom_mc,
        df_K_4mom_mc,
        df_KST_4mom_mc,
        df_mu_p_4mom_mc,
        df_mu_m_4mom_mc,
    )

    # save
    df_B0.to_pickle(output_file_path)

for input_path, output_path in zip(input_file_paths, output_file_paths):
    run_analysis(input_path, output_path)
