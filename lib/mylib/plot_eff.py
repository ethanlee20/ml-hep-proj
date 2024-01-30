

def plot_efficiency(
    data,
    variable,
    q_squared_split,
    num_points,
    title,
    xlabel,
    out_dir_path,
    mc_truth_comp=False,
    **kwargs,
):

    efficiency, bin_middles, errors = eff_and_res.calculate_efficiency(
        data, variable, num_points, q_squared_split
    )

    num_det_events = len(
        pre.preprocess(
            data=data,
            q_squared_split=q_squared_split,
            reconstruction_level="det",
            signal_only=True,
        )
    )

    num_gen_events = len(
        pre.preprocess(
            data=data,
            q_squared_split=q_squared_split,
            reconstruction_level="gen",
        )
    )

    if mc_truth_comp:
        efficiency_mc, bin_middles_mc, errors_mc = eff_and_res.calculate_efficiency(
            data, variable, num_points, q_squared_split, mc=True
        )

    fig, ax = plt.subplots()

    ax.scatter(
        bin_middles, 
        efficiency,
        label=r"\textbf{Calculated}"+f"\nDetector (signal): {num_det_events}\nGenerator: {num_gen_events}",
        color="red",
        alpha=0.5,
        **kwargs,
    )
    ax.errorbar(
        bin_middles,
        efficiency,
        yerr=errors,
        fmt="none",
        capsize=5,
        color="black",
        alpha=0.5,
        **kwargs,
    )

    if mc_truth_comp:
        ax.scatter(
            bin_middles_mc,
            efficiency_mc,
            label=r"\textbf{MC Truth}",
            color="blue",
            alpha=0.5,
            **kwargs,
        )
        ax.errorbar(
            bin_middles_mc,
            efficiency_mc,
            yerr=errors_mc,
            fmt="none",
            capsize=5,
            color="orange",
            alpha=0.5,
            **kwargs,
        )

    if variable=="chi":
        x_axis_in_radians(kind="0 to 2pi")

    ax.legend()
    ax.set_xlim(data[variable].min() - 0.05, data[variable].max() + 0.05)
    ax.set_ymargin(0.25)
    ax.set_ylim(bottom=0, top=0.5)
    ax.set_ylabel(r"$\varepsilon$", rotation=0, labelpad=20)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    file_name = f"q2{q_squared_split}_eff_{variable}.png" 

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name=file_name,
    )


