
def split_by_q_squared(data):
    split_data = {
        'all': data, 
        'med': data[(data['q_squared'] > 1) & (data['q_squared'] < 6)],
    }
    return split_data


def only_signal(data):
    return data[data["isSignal"] == 1] 


def split(data, only_signal=False):
    if not only_signal:
        split_data = split_by_q_squared(data)
        return split_data
    sig_data = only_signal(data)
    split_data = split_by_q_squared(sig_data)
    return split_data


def find_num_events(data, q_squared_split, reconstruction_level, only_signal=False)
    split_data = split(data, only_signal)
    num_events = len(split_data[q_squared_split].loc[reconstruction_level])
    return num_events


reconstruction_levels=["gen", "det"]
