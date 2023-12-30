import os.path
import sys

import pandas as pd

import util
import physics


# Setup
path_input = '../data/2023-12-8_tryingStopDoubleCandidates/mc_events_mu_reconstructed.root:gen'
path_output = '../data/2023-12-8_tryingStopDoubleCandidates/mu_gen_ana.pkl'

df_B0 = util.open_tree(path_input)

df_B_4mom = physics.four_momemtum_dataframe(df_B0[["E", "px", "py", "pz"]])

df_mu_p_4mom = physics.four_momemtum_dataframe(df_B0[["mu_p_E", "mu_p_px", "mu_p_py", "mu_p_pz"]])

df_mu_m_4mom = physics.four_momemtum_dataframe(df_B0[["mu_m_E", "mu_m_px", "mu_m_py", "mu_m_pz"]])

df_K_4mom = physics.four_momemtum_dataframe(df_B0[["K_m_E", "K_m_px", "K_m_py", "K_m_pz"]])

df_KST_4mom = physics.four_momemtum_dataframe(df_B0[["KST0_E", "KST0_px", "KST0_py", "KST0_pz"]])


# Solving

df_B0["q_squared"] = physics.invariant_mass_squared_two_particles(df_mu_p_4mom, df_mu_m_4mom)

df_B0["costheta_mu"] = physics.find_costheta_mu(
    df_mu_p_4mom, df_mu_m_4mom, df_B_4mom
)

df_B0["costheta_K"] = physics.find_costheta_K(df_K_4mom, df_KST_4mom, df_B_4mom)

#df_B0 = df_B0.rename(columns={"cosHelicityAngle__bo0__cm0__bc": "costheta_K_builtin"})

df_B0["coschi"] = physics.find_coschi(
    df_B_4mom, df_K_4mom, df_KST_4mom, df_mu_p_4mom, df_mu_m_4mom
)

df_B0["chi"] = physics.find_chi(
    df_B_4mom,
    df_K_4mom,
    df_KST_4mom,
    df_mu_p_4mom,
    df_mu_m_4mom,
)


# Saving

df_B0.to_pickle(path_output)
