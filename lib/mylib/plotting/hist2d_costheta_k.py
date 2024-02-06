
import iterate
import data_util
import hist_2d


@iterate.over_q_squared_splits
def hist_2d_costheta_k(data, q_squared_split, out_dir):

    var_ys = ["K_p_theta", "K_p_p"]
    plot_names = [
        "hist_2d_costheta_k_" + var_name 
        for var_name in var_ys
    ]
    supylabels = [
        r"$\theta^\text{lab}_K$",
        r"$p^\text{lab}_K$"
    ]
    
    for var_y, plot_name, supylabel in zip(var_ys, plot_names, supylabels):
        my.plot_hist_2d_vars(
            data=data,
            var_x="costheta_K",
            var_y=var_y,
            q_squared_split=q_squared_split,
            suptitle=None,
           	supxlabel=r"$\cos\theta_K$",
           	supylabel=supylabel,
        )
        my.save_fig_and_clear(
           	plots_dir_path,
           	plot_name=plot_name
        )
