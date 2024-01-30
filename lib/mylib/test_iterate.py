import iterate

@iterate.over_q_squared_splits
def print_split(data, q_squared_split):
    print(q_squared_split)
    print(data)


print_split("d")
