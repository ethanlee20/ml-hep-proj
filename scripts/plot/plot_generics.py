
import sys
import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import mylib


mylib.setup_mpl_params_save()


data_dir_path = pathlib.Path(sys.argv[1])
data_filepaths = [data_dir_path.joinpath(path) for path in sys.argv[2:]] 

plots_dir_path = data_dir_path.joinpath('plots')
generic_plots_dir_path = plots_dir_path.joinpath('generic')
generic_plots_dir_path.mkdir(parents=True, exist_ok=True)


def plot_q_squared_range(data, range):
    mylib.plot_signal_and_misrecon(
        df=data,
        var="q_squared",
        is_sig_var="isSignal",
        title=r"$q^2$",
        xlabel=r"GeV$^2$",
	    range=range
    )

    
def plot_cos_theta_mu(data):
    mylib.plot_signal_and_misrecon(
        df=data,
        var="costheta_mu",
        is_sig_var="isSignal",
        title=r"$\cos\theta_\mu$",
        xlabel="",
        range=(-1, 1),
    )


def plot_cos_theta_k(data):
    mylib.plot_signal_and_misrecon(
        df=data,
        var="costheta_K",
        is_sig_var="isSignal",
        title=r"$\cos\theta_K$",
        xlabel="",
        range=(-1, 1),
    )


def plot_chi(data):
    mylib.plot_signal_and_misrecon(
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


def plot_datafile(data_filepath):
    data = pd.read_pickle(data_filepath)

    datafile_plots_path = generic_plots_dir_path.joinpath(data_filepath.stem)
    datafile_plots_path.mkdir(exist_ok=True)
    
    q_squared_cut_names = ('all_q2', 'med_q2')
    q_squared_cut_ranges = ((0, 20), (1, 6))
    q_squared_cut_info = zip(q_squared_cut_names, q_squared_cut_ranges)

    def save_and_close(plot_name, cut_name):
        plt.savefig(
            datafile_plots_path.joinpath(cut_name+'_'+plot_name+'.png'),
            bbox_inches='tight'
        )
        plt.clf()
        
    for cut_name, cut_range in q_squared_cut_info:
        cut_data = data[(data['q_squared'] > cut_range[0]) & (data['q_squared'] < cut_range[1])]
        plot_q_squared_range(cut_data, cut_range)
        save_and_close('q_squared', cut_name)
        plot_cos_theta_mu(cut_data)
        save_and_close('cos_theta_mu', cut_name)
        plot_cos_theta_k(cut_data)
        save_and_close('cos_theta_k', cut_name)
        plot_chi(cut_data)
        save_and_close('chi', cut_name)


for filepath in data_filepaths:
    plot_datafile(filepath)
