
from mylib.utilities.iterate import over_q_squared_splits
from mylib.plotting.core.utils.save import save

from mylib.plotting.hist1d.base_gen_det import plot_gen_det


@over_q_squared_splits
def hist_theta_lab_k(data, out_dir, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="K_p_theta",
        q_squared_split=q_squared_split,
        title=r"$\theta^\text{lab}_K$",
        xlabel=None,
    )
    save("hist_theta_lab_k", q_squared_split, out_dir)