
"""Functions for special relavitiy and particle physics calculations."""


from math import pi, sqrt
import numpy as np
import pandas as pd

from mylib.maths import (
    cosine_angle, 
    cross_product_3d, 
    dot_product, 
    square_matrix_transform, 
    unit_normal, 
    vector_magnitude,
)
from mylib.util import make_bin_edges, min_max, bin_data, count_events, find_bin_middles


def four_momemtum_dataframe(df_with_4_col):
    """
    Create a four-momentum dataframe.

    Create a dataframe where each row represents a four-momentum.
    The columns are well labeled.
    The returned dataframe is a new dataframe.
    """

    df_4mom = df_with_4_col.copy()
    df_4mom.columns = ["E", "px", "py", "pz"]
    return df_4mom


def three_momemtum_dataframe(df_with_3_col):
    """
    Create a three-momentum dataframe.
    
    Create a dataframe where each row represents a three-momentum.
    The columns are well labeled.
    The returned dataframe is a new dataframe.
    """

    df_3mom = df_with_3_col.copy()
    df_3mom.columns = ["px", "py", "pz"]
    return df_3mom


def three_velocity_dataframe(df_with_3_col):
    """
    Create a three-velocity dataframe.
    
    Create a dataframe where each row represents a three-velocity.
    The columns are well labeled.
    The returned dataframe is a new dataframe.
    """
    
    df_3vel = df_with_3_col.copy()
    df_3vel.columns = ["vx", "vy", "vz"]
    return df_3vel


def inv_mass_sq_two_particles(
    df_p1_4mom, df_p2_4mom
):
    """
    Compute the squares of the invariant masses for two particles systems.

    Given the four-momentum dataframe of particle 1 and of particle 2,
    return an invariant masses squared series.
    """

    df_p1_4mom = four_momemtum_dataframe(df_p1_4mom)
    df_p2_4mom = four_momemtum_dataframe(df_p2_4mom)

    df_sum_4mom = df_p1_4mom + df_p2_4mom
    df_sum_E = df_sum_4mom["E"]
    df_sum_3mom = three_momemtum_dataframe(
        df_sum_4mom[["px", "py", "pz"]]
    )
    df_sum_3mom_mag_sq = (
        vector_magnitude(df_sum_3mom) ** 2
    )

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
        .rename(
            columns={"px": "vx", "py": "vy", "pz": "vz"}
        )
    )
    return df_3vel


def compute_gamma(df_3vel):
    """
    Compute a series of Lorentz factors.

    Given a dataframe of three velocities,
    return a series of corresponding Lorentz factors.
    """

    df_3vel = three_velocity_dataframe(df_3vel)
    df_vel_mag = vector_magnitude(df_3vel)
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
    df_vel_mag = vector_magnitude(df_vel3vec)
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
        1
        + (df_gamma - 1)
        * df_vel3vec["vx"] ** 2
        / df_vel_mag**2
    )
    df_boost_matrix["b12"] = (
        (df_gamma - 1)
        * df_vel3vec["vx"]
        * df_vel3vec["vy"]
        / df_vel_mag**2
    )
    df_boost_matrix["b13"] = (
        (df_gamma - 1)
        * df_vel3vec["vx"]
        * df_vel3vec["vz"]
        / df_vel_mag**2
    )
    df_boost_matrix["b20"] = -df_gamma * df_vel3vec["vy"]
    df_boost_matrix["b21"] = (
        (df_gamma - 1)
        * df_vel3vec["vy"]
        * df_vel3vec["vx"]
        / df_vel_mag**2
    )
    df_boost_matrix["b22"] = (
        1
        + (df_gamma - 1)
        * df_vel3vec["vy"] ** 2
        / df_vel_mag**2
    )
    df_boost_matrix["b23"] = (
        (df_gamma - 1)
        * df_vel3vec["vy"]
        * df_vel3vec["vz"]
        / df_vel_mag**2
    )
    df_boost_matrix["b30"] = -df_gamma * df_vel3vec["vz"]
    df_boost_matrix["b31"] = (
        (df_gamma - 1)
        * df_vel3vec["vz"]
        * df_vel3vec["vx"]
        / df_vel_mag**2
    )
    df_boost_matrix["b32"] = (
        (df_gamma - 1)
        * df_vel3vec["vz"]
        * df_vel3vec["vy"]
        / df_vel_mag**2
    )
    df_boost_matrix["b33"] = (
        1
        + (df_gamma - 1)
        * df_vel3vec["vz"] ** 2
        / df_vel_mag**2
    )

    return df_boost_matrix


def boost(df_ref_4mom, df_4vec):
    """
    Lorentz boost a 4-vector.

    Lorentz boost a 4-vector to a frame
    given by a reference 4-momentum vector.
    """

    df_ref_vel = (
        three_velocity_from_four_momentum_dataframe(
            df_ref_4mom
        )
    )
    df_boost_matrix = compute_Lorentz_boost_matrix(
        df_ref_vel
    )
    df_4vec_transformed = square_matrix_transform(
        df_boost_matrix, df_4vec
    )

    return df_4vec_transformed


def find_costheta_ell(df_ell_p_4mom, df_ell_m_4mom, df_B_4mom):
    """
    Find the cosine of the muon helicity angle for B -> K* ell+ ell-.
    """

    df_ell_p_4mom = four_momemtum_dataframe(df_ell_p_4mom)
    df_ell_m_4mom = four_momemtum_dataframe(df_ell_m_4mom)
    df_B_4mom = four_momemtum_dataframe(df_B_4mom)

    df_ellell_4mom = df_ell_p_4mom + df_ell_m_4mom

    df_ell_p_4mom_ellellframe = boost(
        df_ref_4mom=df_ellell_4mom, df_4vec=df_ell_p_4mom
    )
    df_ell_p_3mom_ellellframe = three_momemtum_dataframe(
        df_ell_p_4mom_ellellframe[["px", "py", "pz"]]
    )

    df_ellell_4mom_Bframe = boost(
        df_ref_4mom=df_B_4mom, df_4vec=df_ellell_4mom
    )
    df_ellell_3mom_Bframe = three_momemtum_dataframe(
        df_ellell_4mom_Bframe[["px", "py", "pz"]]
    )

    df_costheta_ell = cosine_angle(
        df_ellell_3mom_Bframe, df_ell_p_3mom_ellellframe
    )

    return df_costheta_ell


def find_costheta_K(df_K_4mom, df_KST_4mom, df_B_4mom):
    """
    Find the cosine of the K* helicity angle for B -> K* ell+ ell-.
    """

    df_K_4mom = four_momemtum_dataframe(df_K_4mom)
    df_KST_4mom = four_momemtum_dataframe(df_KST_4mom)
    df_B_4mom = four_momemtum_dataframe(df_B_4mom)

    df_K_4mom_KSTframe = boost(
        df_ref_4mom=df_KST_4mom, df_4vec=df_K_4mom
    )
    df_K_3mom_KSTframe = three_momemtum_dataframe(
        df_K_4mom_KSTframe[["px", "py", "pz"]]
    )

    df_KST_4mom_Bframe = boost(
        df_ref_4mom=df_B_4mom, df_4vec=df_KST_4mom
    )
    df_KST_3mom_Bframe = three_momemtum_dataframe(
        df_KST_4mom_Bframe[["px", "py", "pz"]]
    )

    df_costheta_K = cosine_angle(
        df_KST_3mom_Bframe, df_K_3mom_KSTframe
    )

    return df_costheta_K


def find_unit_normal_KST_K_plane(
    df_B_4mom, df_KST_4mom, df_K_4mom
):
    """
    Find the unit normal to the plane made by the
    direction vectors of the K* and K.

    This is for B -> K* ell+ ell-.
    """

    df_B_4mom = four_momemtum_dataframe(df_B_4mom)
    df_KST_4mom = four_momemtum_dataframe(df_KST_4mom)
    df_K_4mom = four_momemtum_dataframe(df_K_4mom)

    df_K_4mom_KSTframe = boost(
        df_ref_4mom=df_KST_4mom, df_4vec=df_K_4mom
    )
    df_K_3mom_KSTframe = three_momemtum_dataframe(
        df_K_4mom_KSTframe[["px", "py", "pz"]]
    )
    df_KST_4mom_Bframe = boost(
        df_ref_4mom=df_B_4mom, df_4vec=df_KST_4mom
    )
    df_KST_3mom_Bframe = three_momemtum_dataframe(
        df_KST_4mom_Bframe[["px", "py", "pz"]]
    )

    df_unit_normal_KST_K_plane = unit_normal(
        df_K_3mom_KSTframe, df_KST_3mom_Bframe
    )
    return df_unit_normal_KST_K_plane


def find_unit_normal_ellell_ellplus_plane(
    df_B_4mom, df_ell_p_4mom, df_ell_m_4mom
):
    """
    Find the unit normal to the plane made by
    the direction vectors of the dilepton system and
    the positively charged lepton.

    This is for B -> K* ell+ ell-.
    """

    df_B_4mom = four_momemtum_dataframe(df_B_4mom)
    df_ell_p_4mom = four_momemtum_dataframe(df_ell_p_4mom)
    df_ell_m_4mom = four_momemtum_dataframe(df_ell_m_4mom)

    df_ellell_4mom = df_ell_p_4mom + df_ell_m_4mom

    df_ell_p_4mom_ellellframe = boost(
        df_ref_4mom=df_ellell_4mom, df_4vec=df_ell_p_4mom
    )
    df_ell_p_3mom_ellellframe = three_momemtum_dataframe(
        df_ell_p_4mom_ellellframe[["px", "py", "pz"]]
    )
    df_ellell_4mom_Bframe = boost(
        df_ref_4mom=df_B_4mom, df_4vec=df_ellell_4mom
    )
    df_ellell_3mom_Bframe = three_momemtum_dataframe(
        df_ellell_4mom_Bframe[["px", "py", "pz"]]
    )

    df_unit_normal_ellell_ellplus_plane = unit_normal(
        df_ell_p_3mom_ellellframe, df_ellell_3mom_Bframe
    )
    return df_unit_normal_ellell_ellplus_plane


def find_coschi(
    df_B_4mom,
    df_K_4mom,
    df_KST_4mom,
    df_ell_p_4mom,
    df_ell_m_4mom,
):
    """
    Find the cosine of the decay angle chi.

    Chi is the angle between the K* K decay plane and the dilepton ell+ decay plane.

    This is for B -> K* ell+ ell-.
    """

    df_unit_normal_KST_K_plane = (
        find_unit_normal_KST_K_plane(
            df_B_4mom, df_KST_4mom, df_K_4mom
        )
    )
    df_unit_normal_ellell_ellplus_plane = (
        find_unit_normal_ellell_ellplus_plane(
            df_B_4mom, df_ell_p_4mom, df_ell_m_4mom
        )
    )

    coschi = dot_product(
        df_unit_normal_KST_K_plane,
        df_unit_normal_ellell_ellplus_plane,
    )

    return coschi


def find_chi(
    df_B_4mom,
    df_K_4mom,
    df_KST_4mom,
    df_ell_p_4mom,
    df_ell_m_4mom,
):
    """
    Find the decay angle chi.

    Chi is the angle between the K* K decay plane and the dilepton ell+ decay plane.
    It can range from 0 to 2*pi.

    This is for B -> K* ell+ ell-.
    """

    coschi = find_coschi(
        df_B_4mom,
        df_K_4mom,
        df_KST_4mom,
        df_ell_p_4mom,
        df_ell_m_4mom,
    )

    df_unit_normal_KST_K_plane = (
        find_unit_normal_KST_K_plane(
            df_B_4mom, df_KST_4mom, df_K_4mom
        )
    )
    df_unit_normal_ellell_ellplus_plane = (
        find_unit_normal_ellell_ellplus_plane(
            df_B_4mom, df_ell_p_4mom, df_ell_m_4mom
        )
    )

    n_ell_cross_n_K = cross_product_3d(
        df_unit_normal_ellell_ellplus_plane,
        df_unit_normal_KST_K_plane,
    )

    df_B_4mom = four_momemtum_dataframe(df_B_4mom)
    df_KST_4mom = four_momemtum_dataframe(df_KST_4mom)
    df_KST_4mom_Bframe = boost(
        df_ref_4mom=df_B_4mom, df_4vec=df_KST_4mom
    )
    df_KST_3mom_Bframe = three_momemtum_dataframe(
        df_KST_4mom_Bframe[["px", "py", "pz"]]
    )

    n_ell_cross_n_K_dot_Kst = dot_product(
        n_ell_cross_n_K, df_KST_3mom_Bframe
    )
    chi = np.sign(n_ell_cross_n_K_dot_Kst) * np.arccos(
        coschi
    )

    def to_positive_angles(chi):
        return chi.where(chi > 0, chi + 2 * np.pi)

    chi = to_positive_angles(chi)

    return chi


def calc_dif_inv_mass_k_pi_and_kst(df_K_4mom, df_pi_4mom):
    """
    Calcualate the difference between the invariant mass of the K pi system
    and the K*'s invariant mass (PDG value).
    """

    inv_mass_kst = 0.892

    df_inv_mass_k_pi = np.sqrt(
        inv_mass_sq_two_particles(df_K_4mom, df_pi_4mom)
    )

    dif = df_inv_mass_k_pi - inv_mass_kst
    return dif


def calc_afb_of_q_squared(df, ell, num_points):
    """
    Calcuate Afb as a function of q squared.
    Afb is the forward-backward asymmetry.
    """
    
    def _calc_afb(ell):
        def calc(df):
            if ell == 'mu':
                d_cos_theta_l = df['costheta_mu']
            elif ell == 'e':
                d_cos_theta_l = df['costheta_e']

            f = d_cos_theta_l[(d_cos_theta_l > 0) & (d_cos_theta_l < 1)].count()
            b = d_cos_theta_l[(d_cos_theta_l > -1) & (d_cos_theta_l < 0)].count()
            
            afb = (f - b) / (f + b)

            return afb
        return calc

    def _calc_afb_err(ell):
        def calc(df):
            if ell == 'mu':
                d_cos_theta_l = df['costheta_mu']
            elif ell == 'e':
                d_cos_theta_l = df['costheta_e']


            f = d_cos_theta_l[(d_cos_theta_l > 0) & (d_cos_theta_l < 1)].count()
            b = d_cos_theta_l[(d_cos_theta_l > -1) & (d_cos_theta_l < 0)].count()
            
            f_stdev = sqrt(f)
            b_stdev = sqrt(b)

            afb_stdev = 2*f*b / (f+b)**2 * sqrt((f_stdev/f)**2 + (b_stdev/b)**2)
            afb_err = afb_stdev

            return afb_err
        return calc


    df = df[(df['q_squared']>0) & (df['q_squared']<20)]
    binned, edges = bin_data(df, 'q_squared', num_points, ret_edges=True)
    
    afbs = binned.apply(_calc_afb(ell))
    errs = binned.apply(_calc_afb_err(ell))
    q_squareds = find_bin_middles(edges)

    return q_squareds, afbs, errs


def calc_s5_of_q_squared(df, num_points):
    """
    Calculate S5 as a function of q squared.
    S5 is an angular asymmetry.
    """

    def _calc_s5(df):
        costheta_k = df["costheta_K"]
        chi = df["chi"]
        
        f = count_events(df[
            (((costheta_k > 0) & (costheta_k < 1)) & ((chi > 0) & (chi < pi/2)))
            | (((costheta_k > 0) & (costheta_k < 1)) & ((chi > 3*pi/2) & (chi < 2*pi)))
            | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > pi/2) & (chi < 3*pi/2)))
        ])

        b = count_events(df[
            (((costheta_k > 0) & (costheta_k < 1)) & ((chi > pi/2) & (chi < 3*pi/2)))
            | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > 0) & (chi < pi/2)))
            | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > 3*pi/2) & (chi < 2*pi)))
        ])

        try: 
            s5 = 4/3 * (f - b) / (f + b)
        except ZeroDivisionError:
            print("division by 0, returning nan")
            s5 = np.nan
        
        return s5


    def _calc_s5_err(df):
        costheta_k = df["costheta_K"]
        chi = df["chi"]
        
        f = count_events(df[
            (((costheta_k > 0) & (costheta_k < 1)) & ((chi > 0) & (chi < pi/2)))
            | (((costheta_k > 0) & (costheta_k < 1)) & ((chi > 3*pi/2) & (chi < 2*pi)))
            | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > pi/2) & (chi < 3*pi/2)))
        ])

        b = count_events(df[
            (((costheta_k > 0) & (costheta_k < 1)) & ((chi > pi/2) & (chi < 3*pi/2)))
            | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > 0) & (chi < pi/2)))
            | (((costheta_k > -1) & (costheta_k < 0)) & ((chi > 3*pi/2) & (chi < 2*pi)))
        ])

        f_stdev = sqrt(f)
        b_stdev = sqrt(b)

        try: 
            stdev = 4/3 * 2*f*b / (f+b)**2 * sqrt((f_stdev/f)**2 + (b_stdev/b)**2)
            err = stdev

        except ZeroDivisionError:
            print("division by 0, returning nan")
            err = np.nan
        
        return err

    df = df[(df['q_squared']>0) & (df['q_squared']<20)]
    binned, edges = bin_data(df, 'q_squared', num_points, ret_edges=True)
    s5s = binned.apply(_calc_s5)
    errs = binned.apply(_calc_s5_err)
    q_squareds = find_bin_middles(edges)

    return q_squareds, s5s, errs


def calc_eff(d_gen, d_det, n):
    """
    Calculate the efficiency per bin.

    The efficiency of bin i is defined as the number of
    detector entries in i divided by the number of generator
    entries in i.

    The error for bin i is calculated as the squareroot of the
    number of detector entries in i divided by the number of
    generator entries in i.

    d_gen is a series of generator level values.
    d_det is a series of detector level values.
    n is the number of efficiency datapoints to calculate.
    """
    
    min, max = min_max([d_gen, d_det])
    bin_edges, bin_mids = make_bin_edges(min, max, n, ret_middles=True)

    hist_gen, _ = np.histogram(d_gen, bins=bin_edges)
    hist_det, _ = np.histogram(d_det, bins=bin_edges)

    eff = hist_det / hist_gen
    err = np.sqrt(hist_det) / hist_gen

    return bin_mids, eff, err


def calculate_resolution(data, variable, q_squared_split):
    """
    Calculate the resolution.

    The resolution of a variable is defined as the
    reconstructed value minus the MC truth value.

    If the variable is chi, periodicity is accounted for.
    """

    data_calc = section(data, sig_noise='sig', var=variable, q_squared_split=q_squared_split).loc["det"]
    data_mc = section(data, sig_noise='sig', var=variable+'_mc', q_squared_split=q_squared_split).loc["det"]

    resolution = data_calc - data_mc

    if variable != "chi":
        return resolution

    def apply_periodicity(resolution):
        resolution = resolution.where(
                resolution < np.pi, resolution - 2 * np.pi
        )
        resolution = resolution.where(
            resolution > -np.pi, resolution + 2 * np.pi
        )
        return resolution

    return apply_periodicity(resolution)


