
"""Resolution calculations."""

def calculate_resolution(data, variable, q_squared_split):
    """
    Calculate the resolution.
    
    The resolution of a variable is defined as the 
    reconstructed value minus the MC truth value.
    """
    data_calc = pre.preprocess(data, variables=variable, q_squared_split=q_squared_split, reconstruction_level="det", signal_only=True)
    data_mc = pre.preprocess(data, variables=variable+'_mc', q_squared_split=q_squared_split, reconstruction_level="det", signal_only=True)
    
    resolution = data_calc - data_mc

    if variable != "chi":
        return resolution

    def apply_periodicity(resolution):
        resolution = resolution.where(
                resolution < np.pi, resolution - 2 * np.pi
        )
        resolution = resolution.where(
            resolution > -np.pi, resolution + 2 * np.pi
        )
        return resolution

    return apply_periodicity(resolution)
