import pandas as pd


test_df_a = pd.DataFrame(
    {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}, index=[3, 4, 10]
)


test_df_b = pd.DataFrame(
    {"d": [1, 1, 2], "e": [3, 2, 1], "f": [5, 4, 7]}, index=[3, 4, 10]
)


test_df_vec_a = pd.DataFrame(
    {"v_1": [2, 5, 3], "v_2": [7, 12, 1], "v_3": [1, 4, 2]}, index=[1, 5, 6]
)


test_df_vec_b = pd.DataFrame(
    {"v_1": [4, 5, 1], "v_2": [1, 2, 5], "v_3":[7, 1, 4]}, index = [1, 5, 6]
)


test_df_square_mat = pd.DataFrame(
    {
        "m_11": [4, 1, 3], 
        "m_12": [6, 1, 4],
        "m_13": [8, 5, 5], 
        "m_21": [7, 4, 2], 
        "m_22": [1, 0, 8], 
        "m_23": [7, 10, 4], 
        "m_31": [6, 4, 2], 
        "m_32": [9, 3, 2], 
        "m_33": [9, 2, 7] 
    }, index = [1, 5, 6]
)
 
