import sys
import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import lib.plotting


lib.plotting.setup_mpl_params_save()


path_input_data_gen_level = sys.argv[1]
path_input_data_recon_level = sys.argv[2]
path_output_dir = sys.argv[3]


def make_output_dir(path):
    os.mkdir(path)
try: make_output_dir(path_output_dir)
except: print('could not make output dir')


data_gen_level = pd.read_pickle(path_input_data_gen_level)
split_data_gen_level = dict(
    q2_all=data_gen_level,
    q2_med=data_gen_level[(data_gen_level['q_squared'] > 1) & (data_gen_level['q_squared'] < 6)]
)
data_recon_level = pd.read_pickle(path_input_data_recon_level)
split_data_recon_level = dict(
    q2_all=data_recon_level,
    q2_med=data_recon_level[(data_recon_level['q_squared'] > 1) & (data_recon_level['q_squared'] < 6)]
)


def plot_helicity_angle_mu_efficiency():
    num_data_points = 10
    variable = 'costheta_mu'
    title = r'Efficiency for $\cos\theta_\mu$'
    xlabel = r'$\cos\theta_\mu$'

    for split in split_data_recon_level:
        lib.plotting.plot_efficiency(
            data_recon=split_data_recon_level[split],
            data_gen=split_data_gen_level[split],
            variable=variable,
            num_data_points=num_data_points,
            title=title,
            xlabel=xlabel
        )
        plt.savefig(os.path.join(path_output_dir, f'{split}_eff_costheta_mu.png'), bbox_inches='tight')
        plt.close()


def plot_helicity_angle_K_efficiency():
    num_data_points = 10
    variable = 'costheta_K'
    title = r'Efficiency for $\cos\theta_K$'
    xlabel = r'$\cos\theta_K$'

    for split in split_data_recon_level:
        lib.plotting.plot_efficiency(
            data_recon=split_data_recon_level[split],
            data_gen=split_data_gen_level[split],
            variable=variable,
            num_data_points=num_data_points,
            title=title,
            xlabel=xlabel
        )
        plt.savefig(os.path.join(path_output_dir, f'{split}_eff_costheta_K.png'), bbox_inches='tight')
        plt.close()


def plot_chi_efficiency():
    for split in split_data_recon_level:
        lib.plotting.plot_efficiency(
            data_recon=split_data_recon_level[split],
            data_gen=split_data_gen_level[split],
            variable='chi',
            num_data_points=10,
            title=r'Efficiency for $\chi$',
            xlabel=r'$\chi$'
        )
        plt.xticks(
            [0, np.pi / 2, np.pi, (3 / 2) * np.pi, 2 * np.pi],
            [r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"],
        )
        plt.savefig(os.path.join(path_output_dir, f'{split}_eff_chi.png'), bbox_inches='tight')
        plt.close()


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

        lib.plotting.plot_gen_recon_compare(
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

        lib.plotting.plot_gen_recon_compare(
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


def plot_resolution_costheta_K():
    for split in split_data_recon_level:

        lib.plotting.plot_resolution(
            'costheta_K',
            'costheta_K_gen',
            data=split_data_recon_level[split],
            title=r'Resolution for $\cos\theta_K$',
            xlabel=r'$\cos\theta_{K}^\text{gen} - \cos\theta_{K}^\text{recon}$'
        )
        plt.savefig(
            os.path.join(path_output_dir, f'{split}_res_costheta_K.png'),
            bbox_inches='tight'
        )
        plt.close()


def plot_resolution_costheta_mu():
    for split in split_data_recon_level:

        lib.plotting.plot_resolution(
            'costheta_mu',
            'costheta_mu_gen',
            data=split_data_recon_level[split],
            title=r'Resolution for $\cos\theta_\mu$',
            xlabel=r'$\cos\theta_{\mu}^\text{gen} - \cos\theta_{\mu}^\text{recon}$'
        )
        plt.savefig(
            os.path.join(path_output_dir, f'{split}_res_costheta_mu.png'),
            bbox_inches='tight'
        )
        plt.close()


def plot_resolution_chi():
    for split in split_data_recon_level:

        lib.plotting.plot_resolution(
            'chi',
            'chi_gen',
            data=split_data_recon_level[split],
            title=r'Resolution for $\chi$',
            xlabel=r'$\chi^\text{gen} - \chi^\text{recon}$'
        )
        plt.savefig(
            os.path.join(path_output_dir, f'{split}_res_chi.png'),
            bbox_inches='tight'
        )
        plt.close()



plot_helicity_angle_mu_efficiency()
plot_helicity_angle_K_efficiency()
plot_chi_efficiency()
plot_comparison_costheta_mu()
plot_comparison_costheta_K()
plot_comparison_chi()
plot_resolution_costheta_mu()
plot_resolution_costheta_K()
plot_resolution_chi()
