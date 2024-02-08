from mylib.plotting.hist1d.base_gen_det import plot_gen_det


def hist_theta_lab_k(data, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="K_p_theta",
        q_squared_split=q_squared_split,
        title=r"$\theta^\text{lab}_K$",
        xlabel=None,
    )
    return fig, ax