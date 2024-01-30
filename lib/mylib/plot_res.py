

def plot_resolution(
    data,
    variable,
    q_squared_split,
    title,
    xlabel, 
    out_dir_path,
):

    resolution = eff_and_res.calculate_resolution(
        data,
        variable,
        q_squared_split,
    )

    fig, ax = plt.subplots()
    
    ax.hist(
        resolution,
        label=generate_stats_label(resolution, "Signal Events"),
        bins=approx_num_bins(resolution),
        color="red",
        histtype="step",
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    file_name = f"q2{q_squared_split}_res_{variable}.png"

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name=file_name,
    )
    
