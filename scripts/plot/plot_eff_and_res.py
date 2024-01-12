import sys
import os
import pathlib as pl

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mylib


def get_user_input():
    data_dir_path = pl.Path(sys.argv[1])
    in_file_name = sys.argv[2]    

    return data_dir_path, in_file_name
    

def configure_paths(data_dir_path, in_file_name):
    in_file_path = data_dir_path.joinpath(in_file_name)
    
    plots_dir_name = "plots"
    eff_res_plots_dir_name = "eff_and_res"
    out_dir_path = data_dir_path.joinpath(plots_dir_name, eff_res_plots_dir_name)
    out_dir_path.mkdir(parents=True, exist_ok=True)
    
    return in_file_path, out_dir_path 


def plot_eff(data, out_dir_path):

    num_data_points = 20
    
    for q_squared_split in ["all","med"]:
        mylib.plot_efficiency(
            data=data,
            variable="costheta_mu", 
            q_squared_split=q_squared_split,
            num_data_points=num_data_points,
            title=r"Efficiency for $\cos\theta_\mu$",
            xlabel=r"$\cos\theta_\mu$",
            out_dir_path=out_dir_path
        )

        mylib.plot_efficiency(
            data=data,
            variable="costheta_K", 
            q_squared_split=q_squared_split,
            num_data_points=num_data_points,
            title=r"Efficiency for $\cos\theta_K$",
            xlabel=r"$\cos\theta_K$",
            out_dir_path=out_dir_path
        )

        mylib.plot_efficiency(
            data=data,
            variable="chi", 
            q_squared_split=q_squared_split,
            num_data_points=num_data_points,
            title=r"Efficiency for $\chi$",
            xlabel=r"$\chi$",
            radians=True,
            out_dir_path=out_dir_path
        )


def plot_res(data, out_dir_path):

    mylib.plot_resolution(
        vars=['costheta_mu', 'costheta_K', 'chi'], 
        q_squared_splits=['all', 'med'],
        data=data,
        out_dir_path=out_dir_path,
    )


def main():
    mylib.setup_mpl_params_save()
    in_file_path, out_dir_path = configure_paths(*get_user_input())
    data = pd.read_pickle(in_file_path)
    plot_eff(data, out_dir_path)
    plot_res(data, out_dir_path)


if __name__ == "__main__":
    main()




def plot_resolution_cos_theta_k(data):
    mylib.plot_resolution(
        "costheta_K",
        "costheta_K_mc",
        data=data,
        title=r"Resolution for $\cos\theta_K$",
        xlabel=r"$\cos\theta_{K}^\text{recon} - \cos\theta_{K}^\text{MC truth}$",
    )


def plot_resolution_cos_theta_mu(data):
    mylib.plot_resolution(
        "costheta_mu",
        "costheta_mu_mc",
        data=data,
        title=r"Resolution for $\cos\theta_\mu$",
        xlabel=r"$\cos\theta_{\mu}^\text{recon} - \cos\theta_{\mu}^\text{MC truth}$",
    )


def plot_resolution_chi(data):
    mylib.plot_resolution(
        "chi",
        "chi_mc",
        data=data,
        title=r"Resolution for $\chi$",
        xlabel=r"$\chi^\text{recon} - \chi^\text{MC truth}$",
        periodic=True,
    )


def plot(path_data_gen, path_data_recon):
    data_gen = pd.read_pickle(path_data_gen)
    data_recon = pd.read_pickle(path_data_recon)

    cut_names = ["all_q2", "med_q2"]
    cut_ranges = [(0, 20), (1, 6)]

    def save_and_close(plot_name, cut_name):
        plt.savefig(
            path_eff_and_res_plots_dir.joinpath(
                cut_name + "_" + plot_name + ".png"
            ),
            bbox_inches="tight",
        )
        plt.clf()

    for cut_name, cut_range in zip(cut_names, cut_ranges):
        data_gen_cut = data_gen[
            (data_gen["q_squared"] > cut_range[0])
            & (data_gen["q_squared"] < cut_range[1])
        ]
        data_recon_cut = data_recon[
            (data_recon["q_squared"] > cut_range[0])
            & (data_recon["q_squared"] < cut_range[1])
        ]

        plot_cos_theta_mu_efficiency(
            data_gen_cut, data_recon_cut
        )
        save_and_close("eff_cos_theta_mu", cut_name)
        plot_cos_theta_k_efficiency(
            data_gen_cut, data_recon_cut
        )
        save_and_close("eff_cos_theta_k", cut_name)
        plot_chi_efficiency(data_gen_cut, data_recon_cut)
        save_and_close("eff_chi", cut_name)

        plot_resolution_cos_theta_k(data_recon_cut)
        save_and_close("res_cos_theta_k", cut_name)
        plot_resolution_cos_theta_mu(data_recon_cut)
        save_and_close("res_cos_theta_mu", cut_name)
        plot_resolution_chi(data_recon_cut)
        save_and_close("res_chi", cut_name)




