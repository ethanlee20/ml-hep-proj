
from mylib.util.iter import over_q_squared_splits
from mylib.plot.core.util.save import save

from mylib.plot.core.hist.hist_1d.gen_det.base import plot_gen_det
from mylib.plot.core.looks.annotate import annotate_theta_accept


@over_q_squared_splits
def hist_theta_lab_k(data, out_dir, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="K_p_theta",
        q_squared_split=q_squared_split,
        title=r"$\theta^\text{lab}_K$",
        xlabel=None,
    )

    annotate_theta_accept(ax.get_xlim())

    save("hist_theta_lab_k", q_squared_split, out_dir)


