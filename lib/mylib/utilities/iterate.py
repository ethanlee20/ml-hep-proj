import functools

from mylib.utilities.constants import q_squared_splits


def over_q_squared_splits(f):
    def wrapper(*args, **kwargs):
        for q_squared_split in q_squared_splits:
            f(*args, q_squared_split=q_squared_split, **kwargs)
    return wrapper
