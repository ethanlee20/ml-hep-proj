

import numpy as np


def count_events(dat_ser):
    num_events = len(dat_ser)
    return num_events

    
def split_by_q_squared(data):
    split_data = {
        'all': data, 
        'med': data[(data['q_squared'] > 1) & (data['q_squared'] < 6)],
    }
    return split_data


def only_signal(data):
    return data[data["isSignal"] == 1] 


def section(data, only_sig=True, var=None, q_squared_split=None):
    if only_sig:
        data = only_signal(data)
    if q_squared_split:
        data = split_by_q_squared(data)[q_squared_split]
    if var:
        data = data[var]
    return data



def min_max_over_arrays(ars:list):
    big_ar = np.concatenate(ars, axis=None)
    min = np.nanmin(big_ar)
    max = np.nanmax(big_ar)
    breakpoint()
    return min, max   


def approx_num_bins(data):
    """Approximate the number of bins for a histogram by the length of the data."""
    return round(np.sqrt(len(data)))


# def split(data, only_signal=False):
#     if not only_signal:
#         split_data = split_by_q_squared(data)
#         return split_data
#     sig_data = only_signal(data)
#     split_data = split_by_q_squared(sig_data)
#     return split_data





# reconstruction_levels=["gen", "det"]
