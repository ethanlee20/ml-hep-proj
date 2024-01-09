import sys
import pathlib as pl

import pandas as pd

import mylib


def configure_paths():
	data_dir_path = pl.Path(sys.argv[1])
	in_file_name = sys.argv[2]

	in_file_path = data_dir_path.joinpath(in_file_path)

	plots_dir_name = "plots"
	comp_plots_dir_name = "comp"

	comp_plots_dir_path = data_dir_path.joinpath(plots_dir_name, comp_plots_dir_name)
	comp_plots_dir_path.mkdir(parents=True, exist_ok=True)

	return in_file_path, comp_plots_dir_path


def plot_comparison_costheta_k(data, out_file_path):

    mylib.plot_gen_recon_compare(
        data['gen'],
        data['det'],
        var='costheta_K',
        title=r'Comparison of $\cos\theta_K$',
        xlabel=r'$\cos\theta_K$'
    )
    plt.savefig(
        out_file_path,
        bbox_inches='tight'
    )
    plt.close()


def plot_comparison_costheta_mu(data, out_file_path):

    mylib.plot_gen_recon_compare(
        data['gen'],
        data['det'],
        var='costheta_mu',
        title=r'Comparison of $\cos\theta_\mu$',
        xlabel=r'$\cos\theta_\mu$'
    )
    plt.savefig(
        out_file_path,
        bbox_inches='tight'
    )
    plt.close()



def plot_comparison_chi(data, out_file_path):

    mylib.plot_gen_recon_compare(
        data['gen'],
        data['det'],
        var='chi',
        title=r'Comparison of $\chi$',
        xlabel=r'$\chi$',
        radians=True
    )
    plt.savefig(
		out_file_path,
        bbox_inches='tight'
    )
    plt.close()


def split_data_by_q_squared(data):
	data_all = data
	data_med = data[(data['q_squared'] > 1) & (data['q_squared'] < 6)] 
	return data_all, data_med 


def main():
	in_file_path, comp_plots_dir_path = configure_paths()
	
	data = pd.read_pickle(in_file_path)

	splits = split_data_by_q_squared(data)
	split_names = ('q2_all', 'q2_med')
	
	plot_base_file_names = ('comp_costheta_mu', 'comp_costheta_k', 'comp_chi')
	plot_file_name_suffix = '.png'
	
	for split, split_name in zip(splits, split_names):
	 	out_path_costheta_mu = comp_plots_dir_path.joinpath(f'{split_name}_cos_theta_mu{plot_file_name_suffix})
	 	out_path_costheta_k = comp_plots_dir_path.joinpath(f'{split_name}_cos_theta_k{plot_file_name_suffix})
	 	out_path_chi = comp_plots_dir_path.joinpath(f'{split_name}_chi{plot_file_name_suffix})

		plot_comparison_costheta_mu(split, out_path_costheta_mu)
		plot_comparison_costheta_k(split, out_path_costheta_k)
		plot_comparison_chi(split, out_path_chi)


if __name__ == "__main__":
	main()


"""
def plot_comparison_costheta_K(data, num_bins, out_file_path):
	data_gen = data['gen']['costheta_K']
	data_det = data['det']['costheta_K']
	data_det_basf = data['det']['']
	
    fig, ax = plt.subplots()
    ax.hist(
        data_gen,
        label=f'Generator (Entries: {len(data_gen)})',
        color='purple',
        bins=num_bins,
        histtype='step',
        linestyle='-',
    )
    ax.hist(
        data_det,
        label=f'Reconstructed (Entries: {len(data_det)})',
        color='blue',
        bins=num_bins,
        histtype='step'
    )
    ax.hist(
        data['det']['costheta_K_builtin'],
        label='Reconstructed basf2',
        color='red',
        bins=num_bins,
        histtype='step',
        linestyle='--',
        linewidth=1.2
    )
    ax.set_title(r'Comparison of $\cos\theta_K$')
    ax.set_xlabel(r'$\cos\theta_K$')

    ax.legend()

    plt.savefig(out_file_path, bbox_inches='tight')
    plt.close()
"""
