

def find_num_events(dat_ser):
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


# def split(data, only_signal=False):
#     if not only_signal:
#         split_data = split_by_q_squared(data)
#         return split_data
#     sig_data = only_signal(data)
#     split_data = split_by_q_squared(sig_data)
#     return split_data





# reconstruction_levels=["gen", "det"]
