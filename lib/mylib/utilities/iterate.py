import functools

def over_q_squared_splits(plot_fn):
    @functools.wraps(plot_fn)
    def wrapper(*args, **kwargs):
        q_squared_splits = ["med", "all"]
        for q_squared_split in q_squared_splits:
            plot_fn(*args, q_squared_split=q_squared_split, **kwargs)
    return wrapper
