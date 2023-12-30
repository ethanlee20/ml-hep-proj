import os
import sys

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
print(sys.path)

import maths


def test_unit_normal():
    df = pd.DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}, index=[3, 4, 10]
    )
    print(df)

    df1 = pd.DataFrame(
        {"d": [1, 1, 2], "e": [3, 2, 1], "f": [5, 4, 7]}, index=[3, 4, 10]
    )
    print(df1)

    print(maths.unit_normal(df, df1))


if __name__ == "__main__":
    test_unit_normal()
