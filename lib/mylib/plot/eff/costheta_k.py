
from mylib.util.data import section
from mylib.plot.core.util.save import save
from mylib.util.iter import over_q_squared_splits
from mylib.plot.core.eff.eff import plot_eff
from mylib.plot.core.eff.gen_eff import plot_gen_eff


@over_q_squared_splits
def eff_cos_theta_k(data_all, out_dir, q_squared_split):

    data_gen, data_det = section(data_all, only_sig=True, var="costheta_K", q_squared_split=q_squared_split)

    fig, ax = plot_eff(
        data_gen,
        data_det,
        num_points=100,
        title=r"Efficiency of $\cos\theta_K$",
        xlabel=r"$\cos\theta_K$",
    )
    save("eff_costheta_k", q_squared_split, out_dir)


def cut_theta_accep(data_all, q_squared_split):
    data_gen, _ = section(data_all, only_sig=True, q_squared_split=q_squared_split)
    data_gen_cut = data_gen[(data_gen["K_p_theta"] > 0.25) & (data_gen["K_p_theta"] < 2.625)]
    return data_gen['costheta_K'], data_gen_cut['costheta_K']

    
@over_q_squared_splits
def eff_gen_cos_theta_k_theta_accep(data_all, out_dir, q_squared_split):
    
    data_gen, data_gen_cut = cut_theta_accep(data_all, q_squared_split)

    fig, ax = plot_gen_eff(
        data_gen,
        data_gen_cut,
        num_points=100,
        title=r"Generator Efficiency (cut in $\theta^\text{lab}_K$ acceptance)",
        xlabel=r"$\cos\theta_K$",
    )
    save("eff_gen_costheta_k_cut", q_squared_split, out_dir)

