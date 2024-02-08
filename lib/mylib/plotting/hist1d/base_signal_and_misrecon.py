
import matplotlib.pyplot as plt


def plot_signal_and_misrecon(
    data,
    variable, 
    q_squared_split, 
    reconstruction_level, 
    title, 
    xlabel, 
    out_dir_path, 
    **kwargs
):
    data = pre.preprocess(
        data=data,
        variables=variable,
        q_squared_split=q_squared_split,
        reconstruction_level=reconstruction_level
    )

    signal = data[data["isSignal"] == 1]
    misrecon = data[data["isSignal"] == 0]

    signal_label = generate_stats_label(
        signal, 
        descrp="Signal",
    )
    misrecon_label = generate_stats_label(
        misrecon,
        descrp="Misrecon.",
        show_mean=False,
        show_rms=False,
    )

    bins = approx_num_bins(signal)

    fig, ax = plt.subplots()

    ax.hist(
        signal,
        label=signal_label,
        bins=bins,
        alpha=0.6,
        color="red",
        histtype="stepfilled",
        **kwargs,
    )

    ax.hist(
        misrecon,
        label=misrecon_label,
        bins=bins,
        color="blue",
        histtype="step",
        linewidth=1,
        **kwargs,
    )

    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    if variable == "chi":
        x_axis_in_radians(kind="0 to 2pi")
            
    file_name = f'q2{q_squared_split}_{reconstruction_level}_{variable}.png'

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name=file_name,
    )
