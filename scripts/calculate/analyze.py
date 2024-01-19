import sys
import pathlib as pl

import pandas as pd

import mylib


# Setup


def configure_paths(data_dir_path):
    cut_data_dir_name = 'cut'
    cut_data_dir_path = data_dir_path.joinpath(cut_data_dir_name)
    
    cut_data_file_paths = list(cut_data_dir_path.glob('*.pkl')) 

    analyzed_data_dir_name = "analyzed/"
    analyzed_data_dir_path = data_dir_path.joinpath(analyzed_data_dir_name)
    analyzed_data_dir_path.mkdir(parents=True, exist_ok=True)
    
    analyzed_data_file_paths = [
        analyzed_data_dir_path.joinpath(f"{path.stem}_an.pkl") 
        for path in cut_data_file_paths
    ]

    return cut_data_file_paths, analyzed_data_file_paths


def run_analysis(in_file_path, out_file_path):

    #setup
    df_B0 = mylib.open(in_file_path)
    df_B_4mom = mylib.four_momemtum_dataframe(
        df_B0[["E", "px", "py", "pz"]]
    )
    df_B_4mom_mc = mylib.four_momemtum_dataframe(
        df_B0[["mcE", "mcPX", "mcPY", "mcPZ"]]
    )
    df_mu_p_4mom = mylib.four_momemtum_dataframe(
        df_B0[["mu_p_E", "mu_p_px", "mu_p_py", "mu_p_pz"]]
    )
    df_mu_p_4mom_mc = mylib.four_momemtum_dataframe(
        df_B0[
            [
                "mu_p_mcE",
                "mu_p_mcPX",
                "mu_p_mcPY",
                "mu_p_mcPZ",
            ]
        ]
    )
    df_mu_m_4mom = mylib.four_momemtum_dataframe(
        df_B0[["mu_m_E", "mu_m_px", "mu_m_py", "mu_m_pz"]]
    )
    df_mu_m_4mom_mc = mylib.four_momemtum_dataframe(
        df_B0[
            [
                "mu_m_mcE",
                "mu_m_mcPX",
                "mu_m_mcPY",
                "mu_m_mcPZ",
            ]
        ]
    )
    df_K_4mom = mylib.four_momemtum_dataframe(
        df_B0[["K_p_E", "K_p_px", "K_p_py", "K_p_pz"]]
    )
    df_K_4mom_mc = mylib.four_momemtum_dataframe(
        df_B0[
            ["K_p_mcE", "K_p_mcPX", "K_p_mcPY", "K_p_mcPZ"]
        ]
    )
    df_KST_4mom = mylib.four_momemtum_dataframe(
        df_B0[["KST0_E", "KST0_px", "KST0_py", "KST0_pz"]]
    )
    df_KST_4mom_mc = mylib.four_momemtum_dataframe(
        df_B0[
            [
                "KST0_mcE",
                "KST0_mcPX",
                "KST0_mcPY",
                "KST0_mcPZ",
            ]
        ]
    )
    
    # solve
    df_B0[
        "q_squared"
    ] = mylib.invariant_mass_squared_two_particles(
        df_mu_p_4mom, df_mu_m_4mom
    )
    df_B0[
        "q_squared_mc"
    ] = mylib.invariant_mass_squared_two_particles(
        df_mu_p_4mom_mc, df_mu_m_4mom_mc
    )
    df_B0["costheta_mu"] = mylib.find_costheta_mu(
        df_mu_p_4mom, df_mu_m_4mom, df_B_4mom
    )
    df_B0["costheta_mu_mc"] = mylib.find_costheta_mu(
        df_mu_p_4mom_mc, df_mu_m_4mom_mc, df_B_4mom_mc
    )
    df_B0["costheta_K"] = mylib.find_costheta_K(
        df_K_4mom, df_KST_4mom, df_B_4mom
    )
    df_B0["costheta_K_mc"] = mylib.find_costheta_K(
        df_K_4mom_mc, df_KST_4mom_mc, df_B_4mom_mc
    )
    df_B0["coschi"] = mylib.find_coschi(
        df_B_4mom,
        df_K_4mom,
        df_KST_4mom,
        df_mu_p_4mom,
        df_mu_m_4mom,
    )
    df_B0["coschi_mc"] = mylib.find_coschi(
        df_B_4mom_mc,
        df_K_4mom_mc,
        df_KST_4mom_mc,
        df_mu_p_4mom_mc,
        df_mu_m_4mom_mc,
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

    df_B0.to_pickle(out_file_path)


def main():

    data_dir_path = pl.Path("/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/")
    
    cut_data_file_paths, analyzed_data_file_paths = configure_paths(data_dir_path)

    for cut_path, ana_path in zip(cut_data_file_paths, analyzed_data_file_paths):
        run_analysis(cut_path, ana_path)


if __name__ == "__main__":
    main()
