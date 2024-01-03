import os.path
import sys

import pandas as pd

import mylib


# Setup
data_dir = sys.argv[1]
input_file_name = 'mc_events_mu_reconstructed.root'

data_gen_uncut =  
data_det_cut = 



df_B0 = mylib.open_tree(path_input)

df_B0_sig = df_B0[df_B0['isSignal']==1]

df_B_4mom = physics.four_momemtum_dataframe(df_B0[["E", "px", "py", "pz"]])
df_B_4mom_gen = physics.four_momemtum_dataframe(df_B0_sig[["mcE", "mcPX", "mcPY", "mcPZ"]])

df_mu_p_4mom = physics.four_momemtum_dataframe(df_B0[["mu_p_E", "mu_p_px", "mu_p_py", "mu_p_pz"]])
df_mu_p_4mom_gen = physics.four_momemtum_dataframe(df_B0_sig[["mu_p_mcE", "mu_p_mcPX", "mu_p_mcPY", "mu_p_mcPZ"]])

df_mu_m_4mom = physics.four_momemtum_dataframe(df_B0[["mu_m_E", "mu_m_px", "mu_m_py", "mu_m_pz"]])
df_mu_m_4mom_gen = physics.four_momemtum_dataframe(df_B0_sig[["mu_m_mcE", "mu_m_mcPX", "mu_m_mcPY", "mu_m_mcPZ"]])

df_K_4mom = physics.four_momemtum_dataframe(df_B0[["K_m_E", "K_m_px", "K_m_py", "K_m_pz"]])
df_K_4mom_gen = physics.four_momemtum_dataframe(df_B0_sig[["K_m_mcE", "K_m_mcPX", "K_m_mcPY", "K_m_mcPZ"]])

df_KST_4mom = physics.four_momemtum_dataframe(df_B0[["KST0_E", "KST0_px", "KST0_py", "KST0_pz"]])
df_KST_4mom_gen = physics.four_momemtum_dataframe(df_B0_sig[["KST0_mcE", "KST0_mcPX", "KST0_mcPY", "KST0_mcPZ"]])

# Solving

df_B0["q_squared"] = physics.invariant_mass_squared_two_particles(df_mu_p_4mom, df_mu_m_4mom)
df_B0["q_squared_gen"] = physics.invariant_mass_squared_two_particles(df_mu_p_4mom_gen, df_mu_m_4mom_gen)

df_B0["costheta_mu"] = physics.find_costheta_mu(
    df_mu_p_4mom, df_mu_m_4mom, df_B_4mom
)
df_B0["costheta_mu_gen"] = physics.find_costheta_mu(
    df_mu_p_4mom_gen, df_mu_m_4mom_gen, df_B_4mom_gen
)

df_B0["costheta_K"] = physics.find_costheta_K(df_K_4mom, df_KST_4mom, df_B_4mom)
df_B0["costheta_K_gen"] = physics.find_costheta_K(df_K_4mom_gen, df_KST_4mom_gen, df_B_4mom_gen)

df_B0 = df_B0.rename(columns={"cosHelicityAngle__bo0__cm0__bc": "costheta_K_builtin"})

df_B0["coschi"] = physics.find_coschi(
    df_B_4mom, df_K_4mom, df_KST_4mom, df_mu_p_4mom, df_mu_m_4mom
)
df_B0["coschi_gen"] = physics.find_coschi(
    df_B_4mom_gen, df_K_4mom_gen, df_KST_4mom_gen, df_mu_p_4mom_gen, df_mu_m_4mom_gen
)
# print(physics.find_coschi(
#     df_B_4mom_gen, df_K_4mom_gen, df_KST_4mom_gen, df_mu_p_4mom_gen, df_mu_m_4mom_gen).index.values
# )

df_B0["chi"] = physics.find_chi(
    df_B_4mom,
    df_K_4mom,
    df_KST_4mom,
    df_mu_p_4mom,
    df_mu_m_4mom,
)
df_B0["chi_gen"] = physics.find_chi(
    df_B_4mom_gen,
    df_K_4mom_gen,
    df_KST_4mom_gen,
    df_mu_p_4mom_gen,
    df_mu_m_4mom_gen,
)

# Saving

df_B0.to_pickle(path_output_file)
