from mylib.util.iter import over_q_squared_splits
from mylib.plot.core.util.save import save

from mylib.plot.hist_1d.gen_det.gen_det import plot_gen_det


@over_q_squared_splits
def hist_q_squared(data, out_dir, q_squared_split):
    fig, ax = plot_gen_det(
        data,
        var="q_squared",
        q_squared_split=q_squared_split,
        title=r"$q^2$",
        xlabel="[GeV$^2$]",
    )
    save("hist_q_squared", q_squared_split, out_dir)