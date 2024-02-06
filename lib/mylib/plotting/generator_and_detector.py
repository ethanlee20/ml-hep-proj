def plot_gen_det_compare(
    data,
    variable,
    q_squared_split, 
    title,
    xlabel,
    out_dir_path,
):

    data_gen = pre.preprocess(
        data, 
        variables=variable, 
        q_squared_split=q_squared_split, 
        reconstruction_level="gen"
    )
    data_det = pre.preprocess(
        data, 
        variables=variable, 
        q_squared_split=q_squared_split, 
        reconstruction_level="det", 
        signal_only=True
    )
    
    num_bins = approx_num_bins(data_det)

    fig, ax = plt.subplots()
    ax.hist(
        data_gen,
        label=generate_stats_label(
            data_gen, 
            "Generator"
        ),    
        bins=num_bins,
        color="purple",
        histtype="step",
        linestyle="-",
    )

    ax.hist(
        data_det,
        label=generate_stats_label(
            data_det,
            "Detector (signal)"
        ),    
        bins=num_bins,
        color="blue",
        histtype="step",
    )

    if variable == "chi":
        x_axis_in_radians(kind="0 to 2pi")

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    file_name = f'q2{q_squared_split}_comp_{variable}.png'

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name=file_name,
    )
