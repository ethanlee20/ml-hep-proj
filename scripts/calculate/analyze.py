
"""Calculate required quantities from the raw MC data."""


from mylib.util.util import open_data
from mylib.calc.phys import (
    find_chi,
    find_coschi,
    find_costheta_K,
    find_costheta_ell,
    four_momemtum_dataframe,
    invariant_mass_squared_two_particles,

)


data_path = ''
out_path = ''
ell = ''


if ell == 'mu':
    ell_p_E = 'mu_p_E'
    ell_p_px = 'mu_p_px'
    ell_p_py = 'mu_p_py'
    ell_p_pz = 'mu_p_pz'
    ell_p_mcE = 'mu_p_mcE'
    ell_p_mcPX = 'mu_p_mcPX'
    ell_p_mcPY = 'mu_p_mcPY'
    ell_p_mcPZ = 'mu_p_mcPZ'
    ell_m_E = 'mu_m_E'
    ell_m_px = 'mu_m_px'
    ell_m_py = 'mu_m_py'
    ell_m_pz = 'mu_m_pz'
    ell_m_mcE = 'mu_m_mcE'
    ell_m_mcPX = 'mu_m_mcPX'
    ell_m_mcPY = 'mu_m_mcPY'
    ell_m_mcPZ = 'mu_m_mcPZ'
    costheta_ell = 'costheta_mu'
    costheta_ell_mc = 'costheta_mu_mc'
elif ell == 'e':
    ell_p_E = 'e_p_E'
    ell_p_px = 'e_p_px'
    ell_p_py = 'e_p_py'
    ell_p_pz = 'e_p_pz'
    ell_p_mcE = 'e_p_mcE'
    ell_p_mcPX = 'e_p_mcPX'
    ell_p_mcPY = 'e_p_mcPY'
    ell_p_mcPZ = 'e_p_mcPZ'
    ell_m_E = 'e_m_E'
    ell_m_px = 'e_m_px'
    ell_m_py = 'e_m_py'
    ell_m_pz = 'e_m_pz'
    ell_m_mcE = 'e_m_mcE'
    ell_m_mcPX = 'e_m_mcPX'
    ell_m_mcPY = 'e_m_mcPY'
    ell_m_mcPZ = 'e_m_mcPZ'
    costheta_ell = 'costheta_e'
    costheta_ell_mc = 'costheta_e_mc'
else:
    raise ValueError(f"ell not recognized: {ell}")


data = open_data(data_path)

df_B_4mom = four_momemtum_dataframe(
    data[["E", "px", "py", "pz"]]
)
df_B_4mom_mc = four_momemtum_dataframe(
    data[["mcE", "mcPX", "mcPY", "mcPZ"]]
)
df_ell_p_4mom = four_momemtum_dataframe(
    data[[ell_p_E, ell_p_px, ell_p_py, ell_p_pz]]
)
df_ell_p_4mom_mc = four_momemtum_dataframe(
    data[[ell_p_mcE, ell_p_mcPX, ell_p_mcPY, ell_p_mcPZ]]
)
df_ell_m_4mom = four_momemtum_dataframe(
    data[[ell_m_E, ell_m_px, ell_m_py, ell_m_pz]]
)
df_ell_m_4mom_mc = four_momemtum_dataframe(
    data[[ell_m_mcE, ell_m_mcPX, ell_m_mcPY, ell_m_mcPZ]]
)
df_K_4mom = four_momemtum_dataframe(
    data[["K_p_E", "K_p_px", "K_p_py", "K_p_pz"]]
)
df_K_4mom_mc = four_momemtum_dataframe(
    data[["K_p_mcE", "K_p_mcPX", "K_p_mcPY", "K_p_mcPZ"]]
)
df_KST_4mom = four_momemtum_dataframe(
    data[["KST0_E", "KST0_px", "KST0_py", "KST0_pz"]]
)
df_KST_4mom_mc = four_momemtum_dataframe(
    data[["KST0_mcE", "KST0_mcPX", "KST0_mcPY", "KST0_mcPZ"]]
)


data["q_squared"] = invariant_mass_squared_two_particles(
    df_ell_p_4mom, df_ell_m_4mom
)
data["q_squared_mc"] = invariant_mass_squared_two_particles(
    df_ell_p_4mom_mc, df_ell_m_4mom_mc
)
data[costheta_ell] = find_costheta_ell(
    df_ell_p_4mom, df_ell_m_4mom, df_B_4mom
)
data[costheta_ell_mc] = find_costheta_ell(
    df_ell_p_4mom_mc, df_ell_m_4mom_mc, df_B_4mom_mc
)
data["costheta_K"] = find_costheta_K(
    df_K_4mom, df_KST_4mom, df_B_4mom
)
data["costheta_K_mc"] = find_costheta_K(
    df_K_4mom_mc, df_KST_4mom_mc, df_B_4mom_mc
)
data["coschi"] = find_coschi(
    df_B_4mom,
    df_K_4mom,
    df_KST_4mom,
    df_ell_p_4mom,
    df_ell_m_4mom,
)
data["coschi_mc"] = find_coschi(
    df_B_4mom_mc,
    df_K_4mom_mc,
    df_KST_4mom_mc,
    df_ell_p_4mom_mc,
    df_ell_m_4mom_mc,
)
data["chi"] = find_chi(
    df_B_4mom,
    df_K_4mom,
    df_KST_4mom,
    df_ell_p_4mom,
    df_ell_m_4mom,
)
data["chi_mc"] = find_chi(
    df_B_4mom_mc,
    df_K_4mom_mc,
    df_KST_4mom_mc,
    df_ell_p_4mom_mc,
    df_ell_m_4mom_mc,
)

data.to_pickle(out_path)