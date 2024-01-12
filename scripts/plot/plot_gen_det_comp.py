import sys
import pathlib as pl

import pandas as pd

import mylib


def get_user_input():
    data_dir_path = pl.Path(sys.argv[1])
    in_file_name = sys.argv[2]

    return data_dir_path, in_file_name
    

def configure_paths(data_dir_path, in_file_name):

    in_file_path = data_dir_path.joinpath(in_file_name)

    plots_dir_name = "plots"
    comp_plots_dir_name = "comp"

    comp_plots_dir_path = data_dir_path.joinpath(plots_dir_name, comp_plots_dir_name)
    comp_plots_dir_path.mkdir(parents=True, exist_ok=True)

    return in_file_path, comp_plots_dir_path


def plot(data, comp_plots_dir_path):

    for q_squared_split in ['all', 'med']:
        mylib.plot_gen_det_compare(
            variable='costheta_K',
            data=data,
            q_squared_split=q_squared_split,
            title=r'Comparison of $\cos\theta_K$',
            xlabel=r'',
            out_dir_path=comp_plots_dir_path
        )
        
        mylib.plot_gen_det_compare(
            variable='costheta_mu',
            data=data,
            q_squared_split=q_squared_split,
            title=r'Comparison of $\cos\theta_\mu$',
            xlabel='',
            out_dir_path=comp_plots_dir_path
        )
        
        mylib.plot_gen_det_compare(
            variable='chi',
            data=data,
            q_squared_split=q_squared_split,
            title=r'Comparison of $\chi$',
            xlabel='',
            radians=True,
            out_dir_path=comp_plots_dir_path
        )

        mylib.plot_gen_det_compare(
            variable='q_squared',
            data=data,
            q_squared_split=q_squared_split,
            title=r'Comparison of $q^2$',
            xlabel='GeV$^2$',
            out_dir_path=comp_plots_dir_path
        )


def main():
    mylib.setup_mpl_params_save()

    in_file_path, comp_plots_dir_path = configure_paths(*get_user_input())
    
    data = pd.read_pickle(in_file_path)

    data = data[data["isSignal"]==1]
    
    plot(data, comp_plots_dir_path)


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
