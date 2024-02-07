import functools

from mylib.utilities.constants import q_squared_splits

def over_q_squared_splits(plot_fn):
    def wrapper(*args, **kwargs):
        for q_squared_split in q_squared_splits:
            plot_fn(*args, q_squared_split=q_squared_split, **kwargs)
    return wrapper
