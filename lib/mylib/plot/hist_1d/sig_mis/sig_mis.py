
import matplotlib.pyplot as plt

from mylib.plot.core.util.save import save
from mylib.plot.core.looks.leg import stats_legend
from mylib.util.data import approx_num_bins


# def plot_signal_and_misrecon(
#     data,
#     variable, 
#     q_squared_split, 
#     reconstruction_level, 
#     title, 
#     xlabel, 
#     out_dir_path, 
#     **kwargs
# ):
#     data = pre.preprocess(
#         data=data,
#         variables=variable,
#         q_squared_split=q_squared_split,
#         reconstruction_level=reconstruction_level
#     )

#     signal = data[data["isSignal"] == 1]
#     misrecon = data[data["isSignal"] == 0]

#     signal_label = generate_stats_label(
#         signal, 
#         descrp="Signal",
#     )
#     misrecon_label = generate_stats_label(
#         misrecon,
#         descrp="Misrecon.",
#         show_mean=False,
#         show_rms=False,
#     )

#     bins = approx_num_bins(signal)

#     fig, ax = plt.subplots()

#     ax.hist(
#         signal,
#         label=signal_label,
#         bins=bins,
#         alpha=0.6,
#         color="red",
#         histtype="stepfilled",
#         **kwargs,
#     )

#     ax.hist(
#         misrecon,
#         label=misrecon_label,
#         bins=bins,
#         color="blue",
#         histtype="step",
#         linewidth=1,
#         **kwargs,
#     )

#     ax.legend()
#     ax.set_title(title)
#     ax.set_xlabel(xlabel)

#     if variable == "chi":
#         x_axis_in_radians(kind="0 to 2pi")
            
#     file_name = f'q2{q_squared_split}_{reconstruction_level}_{variable}.png'

#     save_fig_and_clear(
#         out_dir_path=out_dir_path,
#         file_name=file_name,
#     )


def plot_deltaE(data, out_dir):
    sig = data[data["isSignal"]==1].loc["det"]["deltaE"]
    mis = data[data["isSignal"]==0].loc["det"]["deltaE"]
    gen = data.loc["gen"]["deltaE"]


    leg_sig = stats_legend(sig, "Detector: Signal")
    leg_mis = stats_legend(mis, "Detector: Misrecon.", show_mean=False, show_rms=False)
    leg_gen = stats_legend(gen, "Generator")

    n_bins = approx_num_bins(sig)

    fig, ax = plt.subplots()

    ax.hist(
        sig,
        label=leg_sig,
        bins=n_bins,
        alpha=0.6,
        color="red",
        histtype="stepfilled",
    )

    ax.hist(
        mis,
        label=leg_mis,
        bins=n_bins,
        color="blue",
        histtype="step",
        linewidth=1,
    )

    ax.hist(
        gen,
        label=leg_gen,
        bins=n_bins,
        color="orange",
        histtype="step",
        linewidth=1,
        linestyle="--"
    )
    
    ax.legend()
    ax.set_title(r'$\Delta E$')
    ax.set_xlabel(r'[GeV]')

    save("deltaE", q_squared_split='all', out_dir=out_dir)


