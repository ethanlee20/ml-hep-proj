import sys
import os
import pathlib as pl

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import mylib


def init_plotting_settings():
    mylib.setup_mpl_params_save()


def get_user_input():
    data_dir_path = pl.Path(sys.argv[1])
    in_file_name = pl.Path(sys.argv[2])

    return data_dir_path, in_file_name


def configure_paths(data_dir_path, in_file_name):
    in_file_path = data_dir_path.joinpath(in_file_name)

    plots_dir_name = "plots"    
    plots_dir_path = data_dir_path.joinpath(plots_dir_name)

    generic_plots_dir_name = "generic"
    generic_plots_dir_path = plots_dir_path.joinpath(generic_plots_dir_name)
    generic_plots_dir_path.mkdir(parents=True, exist_ok=True)

    return in_file_path, generic_plots_dir_path


def plot(in_file_path, generic_plots_dir_path):
    data = pd.read_pickle(in_file_path)


    for q_squared_slice in ['all', 'med']:
        for reconstruction_level in ['gen', 'det']:

            mylib.plot_signal_and_misrecon(
                var='q_squared',
                df=data,
                q_squared_slice=q_squared_slice,
                reconstruction_level=reconstruction_level,
                title=r'$q^2$',
                xlabel=r'GeV$^2$',
                out_dir_path=generic_plots_dir_path
            )

            mylib.plot_signal_and_misrecon(
                var='costheta_mu',
                df=data,
                q_squared_slice=q_squared_slice,
                reconstruction_level=reconstruction_level,
                title=r'$\cos\theta_\mu$',
                xlabel="",
                out_dir_path=generic_plots_dir_path
            )

            mylib.plot_signal_and_misrecon(
                var='costheta_K',
                df=data,
                q_squared_slice=q_squared_slice,
                reconstruction_level=reconstruction_level,
                title=r'$\cos\theta_K$',
                xlabel="",
                out_dir_path=generic_plots_dir_path
            )

            mylib.plot_signal_and_misrecon(
                var='chi',
                df=data,
                q_squared_slice=q_squared_slice,
                reconstruction_level=reconstruction_level,
                title=r'$\chi$',
                xlabel="",
                radians=True,
                out_dir_path=generic_plots_dir_path
            )


def main():
    init_plotting_settings()    
    plot(*configure_paths(*get_user_input()))
    

if __name__ == "__main__":
    main()
    
