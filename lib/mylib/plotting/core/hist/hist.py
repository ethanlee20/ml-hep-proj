
import numpy as np


def approx_num_bins(data_series):
    return round(np.sqrt(len(data_series)))
