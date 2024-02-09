
from mylib.plotting.core.utils.save import save
from mylib.utilities.iterate import over_q_squared_splits
from mylib.plotting.efficiency.efficiency import plot_efficiency


@over_q_squared_splits
def eff_cos_theta_k(data, out_dir, q_squared_split):
    fig, ax = plot_efficiency(
        data,
        var="costheta_K",
        q_squared_split=q_squared_split,
        num_points=100,
        title=r"Efficiency of $\cos\theta_K$",
        xlabel=r"$\cos\theta_K$",
    )
    save("eff_costheta_k", q_squared_split, out_dir)