import os
import sys
import math

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import maths
import test_df


def test_square_matrix_transform():

    print("test square matrix transform")
    
    df_matrix = test_df.test_df_square_mat
    print(df_matrix)
    
    df_vector = test_df.test_df_vec_a
    print(df_vector)

    res = maths.square_matrix_transform(df_matrix, df_vector)
    print(res, "\n")

    assert res.iloc[0, :].values.tolist() == [58.0, 28.0, 84.0]


def test_dot_product(): 

    print("test dot product")

    df_vec1 = test_df.test_df_vec_a
    print(df_vec1)
    
    df_vec2 = test_df.test_df_vec_b
    print(df_vec2)

    res = maths.dot_product(df_vec1, df_vec2)
    print(res, "\n")

    assert res[1] == 22.0
    

def test_vector_magnitude():

    print("test vector magnitude")

    df_vec = test_df.test_df_vec_a
    print(df_vec)

    res = maths.vector_magnitude(df_vec)
    print(res, "\n")

    assert res[1] == math.sqrt(54)


def test_cosine_angle():

    print("test cosine angle")

    df_vec1 = test_df.test_df_vec_a
    print(df_vec1)

    df_vec2 = test_df.test_df_vec_b
    print(df_vec2)

    res = maths.cosine_angle(df_vec1, df_vec2)
    print(res, "\n")

    assert res[1] == 22/math.sqrt(54*66)


def test_cross_product_3d():

    print("test cross product 3d")

    df_vec1 = test_df.test_df_vec_a
    print(df_vec1)

    df_vec2 = test_df.test_df_vec_b
    print(df_vec2)

    res = maths.cross_product_3d(df_vec1, df_vec2)
    print(res, "\n")

    assert res.loc[1].values.tolist() == [48, -10, -26]
    

def test_unit_normal():

    print("test unit normal")

    df_vec1 = test_df.test_df_vec_a
    print(df_vec1)

    df_vec2 = test_df.test_df_vec_b
    print(df_vec2)

    res = maths.unit_normal(df_vec1, df_vec2)
    print(res, "\n")
   
    assert res.loc[1].values.tolist() == [i / math.sqrt(48**2 + (-10)**2 + (-26)**2) for i in [48, -10, -26]] 


if __name__ == "__main__":
    test_square_matrix_transform()
    test_dot_product()
    test_vector_magnitude()
    test_cosine_angle()
    test_cross_product_3d()
    test_unit_normal()
