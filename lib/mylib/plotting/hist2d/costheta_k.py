
from mylib.utilities.iterate import over_q_squared_splits
from mylib.plotting.core.utils.save import save

from mylib.plotting.hist2d.base import plot_hist_2d


@over_q_squared_splits
def hist_2d_costheta_k_theta_k(data, out_dir, q_squared_split):
    fig, axs = plot_hist_2d(
        data,
        var_x="costheta_K",
        var_y="K_p_theta",
        q_squared_split=q_squared_split,
        xlabel=r"$\cos\theta_K$",
        ylabel=r"$\theta^\text{lab}_K$"
    )
    save("hist2d_costheta_k_theta_k", q_squared_split, out_dir)


@over_q_squared_splits
def hist_2d_costheta_k_p_k(data, out_dir, q_squared_split):
    fig, axs = plot_hist_2d(
        data,
        var_x="costheta_K",
        var_y="K_p_p",
        q_squared_split=q_squared_split,
        xlabel=r"$\cos\theta_K$",
        ylabel=r"$p^\text{lab}_K$"
    )
    save("hist2d_costheta_k_p_k", q_squared_split, out_dir)


# def hist_2d_costheta_k_theta_k_save(data, q_squared_split, out_dir):
#     fig, axs = hist_2d_costheta_k_theta_k(data, q_squared_split)

#     file_name = plot_file_name(
#         "hist_2d_costheta_k_theta_k",
#         q_squared_split
#     )

#     save_fig_and_clear(file_name, out_dir)


    # var_ys = ["K_p_theta", "K_p_p"]
    # plot_names = [
    #     "hist_2d_costheta_k_" + var_name 
    #     for var_name in var_ys
    # ]
    # supylabels = [
    #     r"$\theta^\text{lab}_K$",
    #     r"$p^\text{lab}_K$"
    # ]
    
    # for var_y, plot_name, supylabel in zip(var_ys, plot_names, supylabels):
    #     my.plot_hist_2d_vars(
    #         data=data,
    #         var_x="costheta_K",
    #         var_y=var_y,
    #         q_squared_split=q_squared_split,
    #         suptitle=None,
    #        	supxlabel=r"$\cos\theta_K$",
    #        	supylabel=supylabel,
    #     )
    #     my.save_fig_and_clear(
    #        	plots_dir_path,
    #        	plot_name=plot_name
    #     )
