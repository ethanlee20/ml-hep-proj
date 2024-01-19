import sys
import os
import pathlib as pl

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import mylib


def init_plotting_settings():
    mylib.setup_mpl_params_save()
    

def configure_paths(data_dir_path):
    analyzed_data_dir_name = 'analyzed/'
    analyzed_data_dir_path =  data_dir_path.joinpath(analyzed_data_dir_name)

    plots_dir_name = "plots"    
    plots_dir_path = data_dir_path.joinpath(plots_dir_name)
    plots_dir_path.mkdir(parents=True, exist_ok=True)

    return analyzed_data_dir_path, plots_dir_path


def plot(data_to_plot_dir_path, plots_dir_path):
    data = mylib.open_dir(data_to_plot_dir_path)

    for q_squared_slice in ['all', 'med']:
        for reconstruction_level in ['gen', 'det']:

            mylib.plot_signal_and_misrecon(
                var='q_squared',
                df=data,
                q_squared_slice=q_squared_slice,
                reconstruction_level=reconstruction_level,
                title=r'$q^2$',
                xlabel=r'GeV$^2$',
                out_dir_path=plots_dir_path
            )

            mylib.plot_signal_and_misrecon(
                var='costheta_mu',
                df=data,
                q_squared_slice=q_squared_slice,
                reconstruction_level=reconstruction_level,
                title=r'$\cos\theta_\mu$',
                xlabel="",
                out_dir_path=plots_dir_path
            )

            mylib.plot_signal_and_misrecon(
                var='costheta_K',
                df=data,
                q_squared_slice=q_squared_slice,
                reconstruction_level=reconstruction_level,
                title=r'$\cos\theta_K$',
                xlabel="",
                out_dir_path=plots_dir_path
            )

            mylib.plot_signal_and_misrecon(
                var='chi',
                df=data,
                q_squared_slice=q_squared_slice,
                reconstruction_level=reconstruction_level,
                title=r'$\chi$',
                xlabel="",
                radians=True,
                out_dir_path=plots_dir_path
            )


def main():
    init_plotting_settings()    

    data_dir_path = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/')

    ana_data_dir_path, plot_dir_path = configure_paths(data_dir_path)

    plot(ana_data_dir_path, plot_dir_path)
    

if __name__ == "__main__":
    main()
    
