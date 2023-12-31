import sys
import os
import pathlib

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mylib


mylib.setup_mpl_params_save()


data_dir_path = pathlib.Path(sys.argv[1])
path_data_gen = data_dir_path.joinpath(sys.argv[2])
path_data_recon = data_dir_path.joinpath(sys.argv[3])

path_plots_dir = data_dir_path.joinpath('plots')
path_eff_and_res_plots_dir = path_plots_dir.joinpath('efficiency_and_resolution')
path_eff_and_res_plots_dir.mkdir(parents=True, exist_ok=True)


def plot_cos_theta_mu_efficiency(data_gen, data_recon):
    mylib.plot_efficiency(
        data_recon=data_recon,
        data_gen=data_gen,
        variable='costheta_mu',
        num_data_points=10,
        title=r'Efficiency for $\cos\theta_\mu$',
        xlabel=r'$\cos\theta_\mu$'
    )


def plot_cos_theta_k_efficiency(data_gen, data_recon):
    mylib.plot_efficiency(
        data_recon=data_recon,
        data_gen=data_gen,
        variable='costheta_K',
        num_data_points=10,
        title=r'Efficiency for $\cos\theta_K$',
        xlabel= r'$\cos\theta_K$'
    )


def plot_chi_efficiency(data_gen, data_recon):
    mylib.plot_efficiency(
        data_recon=data_recon,
        data_gen=data_gen,
        variable='chi',
        num_data_points=10,
        title=r'Efficiency for $\chi$',
        xlabel=r'$\chi$'
    )
    plt.xticks(
        [0, np.pi / 2, np.pi, (3 / 2) * np.pi, 2 * np.pi],
        [r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"],
    )


def plot_resolution_cos_theta_k(data):
    mylib.plot_resolution(
        'costheta_K',
        'costheta_K_mc',
        data=data,
        title=r'Resolution for $\cos\theta_K$',
        xlabel=r'$\cos\theta_{K}^\text{gen} - \cos\theta_{K}^\text{recon}$'
    )


def plot_resolution_cos_theta_mu(data):
    mylib.plot_resolution(
        'costheta_mu',
        'costheta_mu_mc',
        data=data,
        title=r'Resolution for $\cos\theta_\mu$',
        xlabel=r'$\cos\theta_{\mu}^\text{gen} - \cos\theta_{\mu}^\text{recon}$'
    )


def plot_resolution_chi(data):
    mylib.plot_resolution(
        'chi',
        'chi_mc',
        data=data,
        title=r'Resolution for $\chi$',
        xlabel=r'$\chi^\text{gen} - \chi^\text{recon}$',
        periodic=True
    )


def plot(path_data_gen, path_data_recon):
    data_gen = pd.read_pickle(path_data_gen)
    data_recon = pd.read_pickle(path_data_recon)
    
    cut_names = ["all_q2", "med_q2"]
    cut_ranges = [(0,20), (1,6)]

    def save_and_close(plot_name, cut_name):
        plt.savefig(path_eff_and_res_plots_dir.joinpath(cut_name + '_' + plot_name + '.png'))
        plt.clf()
        
    for cut_name, cut_range in zip(cut_names, cut_ranges):
        data_gen_cut = data_gen[(data_gen["q_squared"] > cut_range[0]) & (data_gen["q_squared"] < cut_range[1])]
        data_recon_cut = data_recon[(data_recon["q_squared"] > cut_range[0]) & (data_recon["q_squared"] < cut_range[1])]
       
        plot_cos_theta_mu_efficiency(data_gen_cut, data_recon_cut)
        save_and_close('eff_cos_theta_mu', cut_name)
        plot_cos_theta_k_efficiency(data_gen_cut, data_recon_cut)
        save_and_close('eff_cos_theta_k', cut_name)
        plot_chi_efficiency(data_gen_cut, data_recon_cut)
        save_and_close('eff_chi', cut_name)

        plot_resolution_cos_theta_k(data_recon_cut)
        save_and_close('res_cos_theta_k', cut_name)
        plot_resolution_cos_theta_mu(data_recon_cut)
        save_and_close('res_cos_theta_mu', cut_name)
        plot_resolution_chi(data_recon_cut)
        save_and_close('res_chi', cut_name)

plot(path_data_gen, path_data_recon)






"""

def plot_comparison_costheta_K():
    bins = 20

    for split in split_data_recon_level:
        fig, ax = plt.subplots()
        ax.hist(
            split_data_gen_level[split]['costheta_K'],
            label=f'Generator (Entries: {len(split_data_gen_level[split])})',
            color='purple',
            bins=bins,
            histtype='step',
            linestyle='-',
        )
        ax.hist(
            split_data_recon_level[split]['costheta_K'],
            label=f'Reconstructed (Entries: {len(split_data_recon_level[split])})',
            color='blue',
            bins=bins,
            histtype='step'
        )
        ax.hist(
            split_data_recon_level[split]['costheta_K_builtin'],
            label='Reconstructed basf2',
            color='red',
            bins=bins,
            histtype='step',
            linestyle='--',
            linewidth=1.2
        )
        ax.set_title(r'Comparison of $\cos\theta_K$')
        ax.set_xlabel(r'$\cos\theta_K$')

        ax.legend()

        plt.savefig(os.path.join(path_output_dir, f'{split}_comp_costheta_K.png'), bbox_inches='tight')
        plt.close()


def plot_comparison_costheta_mu():
    var = 'costheta_mu'
    xlabel = r'$\cos\theta_\mu$'
    title = r'Comparison of $\cos\theta_\mu$'

    for split in split_data_recon_level:

        mylib.plot_gen_recon_compare(
            split_data_gen_level[split],
            split_data_recon_level[split],
            var,
            title=title,
            xlabel=xlabel
        )
        plt.savefig(
            os.path.join(path_output_dir, f'{split}_comp_{var}.png'),
            bbox_inches='tight'
        )
        plt.close()


def plot_comparison_chi():
    var = 'chi'
    xlabel = r'$\chi$'
    title = r'Comparison of $\chi$'

    for split in split_data_recon_level:

        mylib.plot_gen_recon_compare(
            split_data_gen_level[split],
            split_data_recon_level[split],
            var,
            title=title,
            xlabel=xlabel,
            radians=True
        )
        plt.savefig(
            os.path.join(path_output_dir, f'{split}_comp_{var}.png'),
            bbox_inches='tight'
        )
        plt.close()
"""
