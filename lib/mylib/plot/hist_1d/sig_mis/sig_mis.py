
import matplotlib.pyplot as plt
from mylib.calc.phys import calc_dif_inv_mass_k_pi_and_kst

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

def plot_sig_mis(data, var, title, xlabel, xlim=(None, None)):
    sig = data[data["isSignal"]==1].loc["det"][var]
    mis = data[data["isSignal"]==0].loc["det"][var]

    leg_sig = stats_legend(sig, "Detector: Signal")
    leg_mis = stats_legend(mis, "Detector: Misrecon.", show_mean=False, show_rms=False)

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

    ax.set_xlim(xlim)
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    return fig, ax


def plot_deltaE(data, out_dir):
    fig, ax = plot_sig_mis(
        data, 
        var="deltaE", 
        title=r'$\Delta E$', 
        xlabel=r'[GeV]',
        xlim=(-0.1, 0.1)
    )
    save("deltaE", q_squared_split='all', out_dir=out_dir)


def plot_mbc(data, out_dir):
    fig, ax = plot_sig_mis(
        data,
        var="Mbc",
        title=r"$M_{bc}$",
        xlabel=r"[GeV]",
        xlim=(5.26, 5.30)
    )
    save("mbc", q_squared_split='all', out_dir=out_dir)


def plot_invM(data, out_dir):
    data = data.copy()

    data["invM_K_pi - invM_Kst"] = calc_dif_inv_mass_k_pi_and_kst(data)

    fig, ax = plot_sig_mis(
        data,
        var="invM_K_pi - invM_Kst",
        title=r"$M_{K, \pi} - M_{K^*}$",
        xlabel=r"[GeV]",
        xlim=(-0.2, 0.2)
    )
    save("invM", q_squared_split='all', out_dir=out_dir)

