import sys
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import plotting


path_input = '../data/2023-12-8_tryingStopDoubleCandidates/mu_gen_ana.pkl'
path_output_dir = '../data/2023-12-8_tryingStopDoubleCandidates/plot_mu_gen'

try: os.mkdir(path_output_dir)
except: pass

plotting.setup_mpl_params_save()

data_all = pd.read_pickle(path_input)
data_med =data_all[(data_all['q_squared'] > 1) & (data_all['q_squared'] < 6)]



for label, data, q2_range in [('q2all', data_all, (-0.1,20)), ('q2med', data_med, (1,6))]:
    plotting.plot_signal_and_misrecon(
        df=data,
        var="q_squared",
        is_sig_var="isSignal",
        title=r"$q^2$",
        xlabel=r"GeV$^2$",
	range=q2_range
    )
    plt.savefig(os.path.join(path_output_dir, f"{label}_q_squared.png"), bbox_inches="tight")
    plt.close()

    plotting.plot_signal_and_misrecon(
        df=data,
        var="costheta_mu",
        is_sig_var="isSignal",
        title=r"$\cos\theta_\mu$",
        xlabel="",
        range=(-1, 1),
    )
    plt.savefig(os.path.join(path_output_dir, f"{label}_costheta_mu.png"), bbox_inches="tight")
    plt.close()

    plotting.plot_signal_and_misrecon(
        df=data,
        var="costheta_K",
        is_sig_var="isSignal",
        title=r"$\cos\theta_K$",
        xlabel="",
        range=(-1, 1),
    )
    plt.savefig(os.path.join(path_output_dir, f"{label}_costheta_K.png"), bbox_inches="tight")
    plt.close()

    # plotting.plot_signal_and_misrecon(
    #     df=data,
    #     var="costheta_K_builtin",
    #     is_sig_var="isSignal",
    #     title=r"$\cos\theta_K$ (basf2)",
    #     xlabel="",
    #     range=(-1, 1),
    # )
    # plt.savefig(os.path.join(path_output_dir, f"{label}_costheta_K_builtin.png"), bbox_inches="tight")
    # plt.close()

    #plotting.plot_signal_and_misrecon(
    #    df=data,
    #    var="coschi",
    #    is_sig_var="isSignal",
    #    title=r"$\cos\chi$",
    #    xlabel="",
    #    range=(-1, 1),
    #)
    #plt.savefig(os.path.join(path_output_dir, f"{label}_coschi.png"), bbox_inches="tight")
    #plt.close()

    plotting.plot_signal_and_misrecon(
        df=data,
        var="chi",
        is_sig_var="isSignal",
        title=r"$\chi$",
        xlabel="",
    )
    plt.xticks(
        [0, np.pi / 2, np.pi, (3 / 2) * np.pi, 2 * np.pi],
        [r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"],
    )

    plt.savefig(os.path.join(path_output_dir, f'{label}_chi.png'), bbox_inches="tight")
    plt.close()









# for split in image_file_paths:
#     plotting.plot_image(
#         image_file_paths[split],
#         "costheta_mu_bin",
#         "costheta_K_bin",
#         "chi_bin",
#         "q_squared",
#         len(data[split]),
#     )
#     plt.savefig(out_dir[split] + "image.png", bbox_inches="tight", pad_inches=0.4)
#     plt.close()

"""def plot_costheta_K_comparison(data):
    plt.hist(
        data[data["isSignal"] == 1]["costheta_K"],
        label="My Calc. (sig. only)",
        histtype="step",
        bins=25,
        color="red",
        alpha=0.8,
    )
    plt.hist(
        data[data["isSignal"] == 1]["costheta_K_builtin"],
        label="basf2 (sig. only)",
        histtype="step",
        bins=25,
        color="blue",
        alpha=0.8,
    )
    plt.legend()
    plt.title(r"$\cos \theta_K$ Comparison ($q^2 > 15$ GeV$^2$)")
    plt.savefig("./Plots/q2_high/costheta_K_compare.png", bbox_inches="tight")
    print("Plotted costheta_K comparison")
    plt.clf()


def plot_hist2d_costheta_mu_and_q_squared(data):
    plt.hist2d(data["q_squared"], data["costheta_mu"], bins=25, cmap="magma")
    plt.colorbar()
    plt.xlabel(r"$q^2$ [GeV$^2$]")
    plt.ylabel(r"$\cos\theta_\mu$")
    plt.title(r"($q^2 > 15$ GeV$^2$)")
    plt.savefig("./Plots/q2_high/costheta_mu_q2_plot.png", bbox_inches="tight")
    print("Plotted 2d hist costheta_mu and q_squared")
    plt.clf()


def plot_hist2d_costheta_K_and_q_squared(data):
    plt.hist2d(data["q_squared"], data["costheta_K"], bins=25, cmap="magma")
    plt.colorbar()
    plt.xlabel(r"$q^2$ [GeV$^2$]")
    plt.ylabel(r"$\cos\theta_K$ \small{(My Calc.)}")
    plt.title(r"($q^2 > 15$ GeV$^2$)")
    plt.savefig("./Plots/q2_high/costheta_K_q2_plot.png", bbox_inches="tight")
    print("Plotted 2d hist costheta_K and q_squared")
    plt.clf()


def plot_hist2d_coschi_and_q_squared(data):
    plt.hist2d(data["q_squared"], data["coschi"], bins=25, cmap="magma")
    plt.colorbar()
    plt.xlabel(r"$q^2$ [GeV$^2$]")
    plt.ylabel(r"$\cos\chi$")
    plt.title(r"($q^2 > 15$ GeV$^2$)")
    plt.savefig("./Plots/q2_high/coschi_q2_plot.png", bbox_inches="tight")
    print("Plotted 2d hist coschi and q_squared")
    plt.clf()

"""
