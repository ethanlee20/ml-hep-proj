

def apply_q_squared_split(data, q_squared_region):
    """Split the data by q squared value."""
    if q_squared_region == "med":
        return data[(data['q_squared']>1)&(data['q_squared']<6)]
    elif q_squared_region == "all":
        return data
    else: raise ValueError(f"Unrecognized region: {q_squared_region}")


def apply_reconstruction_level_split(data, level):
    """Split the data by reconstruction level."""
    if level == "gen":
        return data.loc["gen"]
    elif level == "det":
        return data.loc["det"]
    else: raise ValueError(f"Unrecognized level: {level}")


def preprocess(data, variables=None,  q_squared_region=None, reconstruction_level=None, signal_only=False):

    if q_squared_region:
        data = apply_q_squared_split(data, q_squared_region)
    if reconstruction_level:
        data = apply_reconstruction_level_split(data, reconstruction_level)
    if signal_only:
        data = data[data["isSignal"] == 1]
    if variable:
        data = data[variable]
    return data
