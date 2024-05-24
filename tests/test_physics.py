import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(__file__), "../")
)

import physics
import test_df


def test_four_momemtum_dataframe():
    print(test_four_momentum_dataframe.__name__)

    df_4vec = test_df.test_df_4vec_a
    df_4mom = physics.four_momentum_dataframe(df_4vec)

    print(df_4mom)


def test_three_momentum_dataframe():
    print(test_three_momentum_dataframe.__name__)

    df_3vec = test_df.test_df_vec_a
    df_3mom = physics.three_momentum_dataframe(df_3vec)

    print(df_3mom)


def test_three_velocity_dataframe():
    print(test_three_velocity_dataframe.__name__)

    df_3vec = test_df.test_df_vec_a
    df_3vel = physics.three_velocity_dataframe(df_3vec)

    print(df_3vel)


def test_invariant_mass_squared_two_particles():
    print(
        test_invariant_mass_squared_two_particles.__name__
    )

    df_4mom_p1 = test_df.test_df_4mom_a
    df_4mom_p2 = test_df.test_df_4mom_b

    inv_m_sq = physics.invariant_mass_squared_two_particles(
        df_4mom_p1, df_4mom_p2
    )

    print(inv_m_sq)


def test_three_velocity_from_four_momentum_dataframe():
    print(
        test_three_velocity_from_four_momentum_dataframe.__name__
    )

    df_4mom = test_df.test_df_4mom_a
    df_3vel = (
        physics.three_velocity_from_four_momentum_dataframe(
            df_4mom
        )
    )

    print(df_3vel)


def test_compute_gamma():
    print(test_compute_gamma.__name__)

    df_3vel = test_df.test_df_vec_a
    df_gamma = physics.compute_gamma(df_3vel)

    print(gamma)


def test_compute_Lorentz_boost_matrix():
    print(test_compute_Lorentz_boost_matrix.__name__)

    df_3vel = test_df.test_df_vec_a
    df_boost_mat = compute_Lorentz_boost_matrix(df_3vel)

    print(df_boost_mat)


def test_boost():
    print(test_boost.__name__)

    df_ref_4mom = test_df.test_df_4mom_a
    df_4vec = test_df.test_df_4vec_a

    boosted = physics.boost(df_ref_4mom, df_4vec)

    print(boosted)


def test_find_costheta_mu():
    print(test_find_costheta_mu.__name__)

    df_4mom_mu_p = test_df.test_df_4mom_a
    df_4mom_mu_m = test_df.test_df_4mom_b
    df_4mom_B = test_df.test_df_4vec_a

    cos_theta_mu = physics.find_costheta_mu(
        df_4mom_mu_p, df_4mom_mu_m, df_4mom_B
    )

    print(cos_theta_mu)


def test_find_costheta_K():
    print(test_find_costheta_K.__name__)

    df_4mom_K = test_df.test_df_4mom_a
    df_4mom_KST = test_df.test_df_4mom_b
    df_4mom_B = test_df.test_df_4vec_a

    cos_theta_K = physics.find_costheta_K(
        df_4mom_K, df_4mom_KST, df_4mom_B
    )

    print(cos_theta_K)


def test_find_unit_normal_KST_K_plane():
    print(test_find_unit_normal_KST_K_plane.__name__)

    df_4mom_B = test_df.test_df_4mom_a
    df_4mom_KST = test_df.test_df_4mom_b
    df_4mom_K = test_df.test_df_4vec_a

    df_norm = physics.find_unit_normal_KST_K_plane(
        df_4mom_B, df_4mom_KST, df_4mom_K
    )

    print(df_norm)


def test_find_unit_normal_mumu_muplus_plane():
    print(test_find_unit_normal_mumu_muplus_plane.__name__)

    df_4mom_B = test_df.test_df_4mom_a
    df_4mom_mu_p = test_df.test_df_4mom_b
    df_4mom_mu_m = test_df.test_df_4vec_a

    df_norm = physics.find_unit_normal_mumu_muplus_plane(
        df_4mom_B, df_4mom_mu_p, df_4mom_mu_m
    )

    print(df_norm)


if __name__ == "__main__":
    test_four_momentum_dataframe()
