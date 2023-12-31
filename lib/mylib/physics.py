
"""Functions for special relavitiy and particle physics calculations."""

import os
import sys

import numpy as np
import pandas as pd

import maths


def four_momemtum_dataframe(df_with_4_col):
    """
    Create a four-momentum dataframe.

    Create a four-momentum dataframe with well-labeled columns.
    The returned dataframe is separate from the input dataframe.
    """

    df_4mom = df_with_4_col.copy()
    df_4mom.columns = ["E", "px", "py", "pz"]
    return df_4mom


def three_momemtum_dataframe(df_with_3_col):
    """
    Create a three-momentum dataframe.

    Create a three-momentum dataframe with well-labeled columns.
    The returned dataframe is separate from the input dataframe.
    """

    df_3mom = df_with_3_col.copy()
    df_3mom.columns = ["px", "py", "pz"]
    return df_3mom


def three_velocity_dataframe(df_with_3_col):
    """
    Create a three-velocity dataframe.

    Create a three-velocity dataframe with well-labeled columns.
    The new dataframe is separate from the input dataframe.
    """

    df_3vel = df_with_3_col.copy()
    df_3vel.columns = ["vx", "vy", "vz"]
    return df_3vel


def invariant_mass_squared_two_particles(df_p1_4mom, df_p2_4mom):
    """
    Compute the squares of the invariant masses for two particles systems.

    Given the four-momentum dataframes of particle 1 and particle 2,
    return a series of the invariant masses squared (computed row-wise).
    """

    df_p1_4mom = four_momemtum_dataframe(df_p1_4mom)
    df_p2_4mom = four_momemtum_dataframe(df_p2_4mom)

    df_sum_4mom = df_p1_4mom + df_p2_4mom
    df_sum_E = df_sum_4mom["E"]
    df_sum_3mom = three_momemtum_dataframe(df_sum_4mom[["px", "py", "pz"]])
    df_sum_3mom_mag_sq = maths.vector_magnitude(df_sum_3mom) ** 2

    df_invM_sq = df_sum_E**2 - df_sum_3mom_mag_sq
    return df_invM_sq


def three_velocity_from_four_momentum_dataframe(df_4mom):
    """
    Compute a three-velocity dataframe from a four-momentum dataframe.
    """

    df_4mom = four_momemtum_dataframe(df_4mom)
    df_relativistic_3mom = df_4mom[["px", "py", "pz"]]
    df_E = df_4mom["E"]
    df_3vel = (
        df_relativistic_3mom.copy()
        .multiply(1 / df_E, axis=0)
        .rename(columns={"px": "vx", "py": "vy", "pz": "vz"})
    )
    return df_3vel


def compute_gamma(df_3vel):
    """
    Compute a series of Lorentz factors.

    Given a dataframe of three velocities,
    return a series of corresponding Lorentz factors.
    """

    df_3vel = three_velocity_dataframe(df_3vel)
    df_vel_mag = maths.vector_magnitude(df_3vel)
    df_gamma = 1 / np.sqrt(1 - df_vel_mag**2)

    return df_gamma


def compute_Lorentz_boost_matrix(df_vel3vec):
    """
    Compute a dataframe of Lorentz boost matricies.

    Given a three velocity dataframe, compute the
    corresponding dataframe of Lorentz boost matricies.
    Each row contains a different matrix.
    """

    df_vel3vec = df_vel3vec.copy()
    df_vel3vec.columns = ["vx", "vy", "vz"]
    df_vel_mag = maths.vector_magnitude(df_vel3vec)
    df_gamma = compute_gamma(df_vel3vec)

    df_boost_matrix = pd.DataFrame(
        data=np.zeros(shape=(df_vel3vec.shape[0], 16)),
        index=df_vel3vec.index,
        columns=[
            "b00",
            "b01",
            "b02",
            "b03",
            "b10",
            "b11",
            "b12",
            "b13",
            "b20",
            "b21",
            "b22",
            "b23",
            "b30",
            "b31",
            "b32",
            "b33",
        ],
    )

    df_boost_matrix["b00"] = df_gamma
    df_boost_matrix["b01"] = -df_gamma * df_vel3vec["vx"]
    df_boost_matrix["b02"] = -df_gamma * df_vel3vec["vy"]
    df_boost_matrix["b03"] = -df_gamma * df_vel3vec["vz"]
    df_boost_matrix["b10"] = -df_gamma * df_vel3vec["vx"]
    df_boost_matrix["b11"] = (
        1 + (df_gamma - 1) * df_vel3vec["vx"] ** 2 / df_vel_mag**2
    )
    df_boost_matrix["b12"] = (
        (df_gamma - 1) * df_vel3vec["vx"] * df_vel3vec["vy"] / df_vel_mag**2
    )
    df_boost_matrix["b13"] = (
        (df_gamma - 1) * df_vel3vec["vx"] * df_vel3vec["vz"] / df_vel_mag**2
    )
    df_boost_matrix["b20"] = -df_gamma * df_vel3vec["vy"]
    df_boost_matrix["b21"] = (
        (df_gamma - 1) * df_vel3vec["vy"] * df_vel3vec["vx"] / df_vel_mag**2
    )
    df_boost_matrix["b22"] = (
        1 + (df_gamma - 1) * df_vel3vec["vy"] ** 2 / df_vel_mag**2
    )
    df_boost_matrix["b23"] = (
        (df_gamma - 1) * df_vel3vec["vy"] * df_vel3vec["vz"] / df_vel_mag**2
    )
    df_boost_matrix["b30"] = -df_gamma * df_vel3vec["vz"]
    df_boost_matrix["b31"] = (
        (df_gamma - 1) * df_vel3vec["vz"] * df_vel3vec["vx"] / df_vel_mag**2
    )
    df_boost_matrix["b32"] = (
        (df_gamma - 1) * df_vel3vec["vz"] * df_vel3vec["vy"] / df_vel_mag**2
    )
    df_boost_matrix["b33"] = (
        1 + (df_gamma - 1) * df_vel3vec["vz"] ** 2 / df_vel_mag**2
    )

    return df_boost_matrix


def boost(df_ref_4mom, df_4vec):
    """
    Lorentz boost a 4-vector.

    Lorentz boost a 4-vector to a frame
    given by a reference 4-momentum vector.
    """

    df_ref_vel = three_velocity_from_four_momentum_dataframe(df_ref_4mom)
    df_boost_matrix = compute_Lorentz_boost_matrix(df_ref_vel)
    df_4vec_transformed = maths.square_matrix_transform(df_boost_matrix, df_4vec)

    return df_4vec_transformed


def find_costheta_mu(df_mu_p_4mom, df_mu_m_4mom, df_B_4mom):
    """
    Find the cosine of the muon helicity angle for B -> K* mu+ mu-.
    """

    df_mu_p_4mom = four_momemtum_dataframe(df_mu_p_4mom)
    df_mu_m_4mom = four_momemtum_dataframe(df_mu_m_4mom)
    df_B_4mom = four_momemtum_dataframe(df_B_4mom)

    df_mumu_4mom = df_mu_p_4mom + df_mu_m_4mom

    df_mu_p_4mom_mumuframe = boost(df_ref_4mom=df_mumu_4mom, df_4vec=df_mu_p_4mom)
    df_mu_p_3mom_mumuframe = three_momemtum_dataframe(
        df_mu_p_4mom_mumuframe[["px", "py", "pz"]]
    )

    df_mumu_4mom_Bframe = boost(df_ref_4mom=df_B_4mom, df_4vec=df_mumu_4mom)
    df_mumu_3mom_Bframe = three_momemtum_dataframe(
        df_mumu_4mom_Bframe[["px", "py", "pz"]]
    )

    df_costheta_mu = maths.cosine_angle(df_mumu_3mom_Bframe, df_mu_p_3mom_mumuframe)

    return df_costheta_mu


def find_costheta_K(df_K_4mom, df_KST_4mom, df_B_4mom):
    """
    Find the cosine of the K* helicity angle for B -> K* mu+ mu-.
    """

    df_K_4mom = four_momemtum_dataframe(df_K_4mom)
    df_KST_4mom = four_momemtum_dataframe(df_KST_4mom)
    df_B_4mom = four_momemtum_dataframe(df_B_4mom)

    df_K_4mom_KSTframe = boost(df_ref_4mom=df_KST_4mom, df_4vec=df_K_4mom)
    df_K_3mom_KSTframe = three_momemtum_dataframe(
        df_K_4mom_KSTframe[["px", "py", "pz"]]
    )

    df_KST_4mom_Bframe = boost(df_ref_4mom=df_B_4mom, df_4vec=df_KST_4mom)
    df_KST_3mom_Bframe = three_momemtum_dataframe(
        df_KST_4mom_Bframe[["px", "py", "pz"]]
    )

    df_costheta_K = maths.cosine_angle(df_KST_3mom_Bframe, df_K_3mom_KSTframe)

    return df_costheta_K


def find_unit_normal_KST_K_plane(df_B_4mom, df_KST_4mom, df_K_4mom):
    """
    Find the unit normal to the plane made by the
    direction vectors of the K* and K.

    This is for B -> K* mu+ mu-.
    """

    df_B_4mom = four_momemtum_dataframe(df_B_4mom)
    df_KST_4mom = four_momemtum_dataframe(df_KST_4mom)
    df_K_4mom = four_momemtum_dataframe(df_K_4mom)

    df_K_4mom_KSTframe = boost(df_ref_4mom=df_KST_4mom, df_4vec=df_K_4mom)
    df_K_3mom_KSTframe = three_momemtum_dataframe(
        df_K_4mom_KSTframe[["px", "py", "pz"]]
    )
    df_KST_4mom_Bframe = boost(df_ref_4mom=df_B_4mom, df_4vec=df_KST_4mom)
    df_KST_3mom_Bframe = three_momemtum_dataframe(
        df_KST_4mom_Bframe[["px", "py", "pz"]]
    )

    df_unit_normal_KST_K_plane = maths.unit_normal(
        df_K_3mom_KSTframe, df_KST_3mom_Bframe
    )
    return df_unit_normal_KST_K_plane


def find_unit_normal_mumu_muplus_plane(df_B_4mom, df_mu_p_4mom, df_mu_m_4mom):
    """
    Find the unit normal to the plane made by
    the direction vectors of the dimuon system and
    the mu+.

    This is for B -> K* mu+ mu-.
    """

    df_B_4mom = four_momemtum_dataframe(df_B_4mom)
    df_mu_p_4mom = four_momemtum_dataframe(df_mu_p_4mom)
    df_mu_m_4mom = four_momemtum_dataframe(df_mu_m_4mom)

    df_mumu_4mom = df_mu_p_4mom + df_mu_m_4mom

    df_mu_p_4mom_mumuframe = boost(df_ref_4mom=df_mumu_4mom, df_4vec=df_mu_p_4mom)
    df_mu_p_3mom_mumuframe = three_momemtum_dataframe(
        df_mu_p_4mom_mumuframe[["px", "py", "pz"]]
    )
    df_mumu_4mom_Bframe = boost(df_ref_4mom=df_B_4mom, df_4vec=df_mumu_4mom)
    df_mumu_3mom_Bframe = three_momemtum_dataframe(
        df_mumu_4mom_Bframe[["px", "py", "pz"]]
    )

    df_unit_normal_mumu_muplus_plane = maths.unit_normal(
        df_mu_p_3mom_mumuframe, df_mumu_3mom_Bframe
    )
    return df_unit_normal_mumu_muplus_plane


def find_coschi(df_B_4mom, df_K_4mom, df_KST_4mom, df_mu_p_4mom, df_mu_m_4mom):
    """
    Find the cosine of the decay angle chi.

    Chi is the angle between the K* K decay plane and the dimuon mu+ decay plane.

    This is for B -> K* mu+ mu-.
    """

    df_unit_normal_KST_K_plane = find_unit_normal_KST_K_plane(
        df_B_4mom, df_KST_4mom, df_K_4mom
    )
    df_unit_normal_mumu_muplus_plane = find_unit_normal_mumu_muplus_plane(
        df_B_4mom, df_mu_p_4mom, df_mu_m_4mom
    )

    coschi = maths.dot_product(
        df_unit_normal_KST_K_plane, df_unit_normal_mumu_muplus_plane
    )

    return coschi


def find_chi(
    df_B_4mom,
    df_K_4mom,
    df_KST_4mom,
    df_mu_p_4mom,
    df_mu_m_4mom,
):
    """
    Find the decay angle chi.

    Chi is the angle between the K* K decay plane and the dimuon mu+ decay plane.
    It can range from 0 to 2*pi.

    This is for B -> K* mu+ mu-.
    """

    coschi = find_coschi(df_B_4mom, df_K_4mom, df_KST_4mom, df_mu_p_4mom, df_mu_m_4mom)

    df_unit_normal_KST_K_plane = find_unit_normal_KST_K_plane(
        df_B_4mom, df_KST_4mom, df_K_4mom
    )
    df_unit_normal_mumu_muplus_plane = find_unit_normal_mumu_muplus_plane(
        df_B_4mom, df_mu_p_4mom, df_mu_m_4mom
    )

    n_mu_cross_n_K = maths.cross_product_3d(
        df_unit_normal_mumu_muplus_plane, df_unit_normal_KST_K_plane
    )

    df_B_4mom = four_momemtum_dataframe(df_B_4mom)
    df_KST_4mom = four_momemtum_dataframe(df_KST_4mom)
    df_KST_4mom_Bframe = boost(df_ref_4mom=df_B_4mom, df_4vec=df_KST_4mom)
    df_KST_3mom_Bframe = three_momemtum_dataframe(
        df_KST_4mom_Bframe[["px", "py", "pz"]]
    )

    n_mu_cross_n_K_dot_Kst = maths.dot_product(n_mu_cross_n_K, df_KST_3mom_Bframe)
    chi = np.sign(n_mu_cross_n_K_dot_Kst) * np.arccos(coschi)

    def to_positive_angles(chi):
        return chi.where(chi > 0, chi + 2 * np.pi)

    chi = to_positive_angles(chi)

    return chi
