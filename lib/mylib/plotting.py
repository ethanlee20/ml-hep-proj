import pathlib as pl
import itertools

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import eff_and_res
import preprocess as pre
import util




    save_fig_and_clear(
        out_dir_path=out_dir,
        file_name=file_name
    )

        
def generate_plot_info(
    variables,
    xlabels,
    titles,
    q_squared_splits,
):

    info = [ (variable, xlabel, title, q_squared_split) 
        for (variable, xlabel, title), q_squared_split 
        in itertools.product(
            zip(variables, xlabels, titles), 
            q_squared_splits
        )
    ]     
    return info

def plot(
    plots, 
    data,
    out_dir_path
):
    """
    Plot given plot types.
    
    Possible plot types include: efficiency, resolution, generics, candidate multiplicity.
    
    Note: Assumes data contains generator and detector events
    as well as all regions of q squared.
    """
    if "efficiency" in plots:
        print("Plotting efficiency.")
        info = generate_plot_info(
            variables = ["costheta_K", "costheta_mu", "chi"],
            xlabels = [r"$\cos\theta_K$", r"$\cos\theta_\mu$", r"$\chi$"],
            titles = [r"Efficiency of $\cos\theta_K$", r"Efficiency of $\cos\theta_\mu$", r"Efficiency of $\chi$"],
            q_squared_splits = ["all", "med"],
        )
        
        for variable, xlabel, title, q_squared_split in info:
            plot_efficiency(
                data=data,
                variable=variable,
                q_squared_split=q_squared_split,
                num_points=100,
                title=title,
                xlabel=xlabel,
                out_dir_path=out_dir_path,
                mc_truth_comp=True,
            )

    if "resolution" in plots:
        print("Plotting resolution.")
        info = generate_plot_info(
            variables = ["costheta_K", "costheta_mu", "chi"],
            xlabels = [r"$\cos\theta_K - \cos\theta_K^{MC}$", r"$\cos\theta_\mu - \cos\theta_\mu^{MC}$", r"$\chi - \chi^{MC}$"],
            titles = [r"Resolution of $\cos\theta_K$", r"Resolution of $\cos\theta_\mu$", r"Resolution of $\chi$"],
            q_squared_splits = ["all", "med"],
        )
                
        [ 
            plot_resolution(
                data=data,
                variable=variable,
                q_squared_split=q_squared_split,
                title=title,
                xlabel=xlabel,
                out_dir_path=out_dir_path,
            )
            for variable, xlabel, title, q_squared_split in info
        ]

    if "candidate multiplicity" in plots:
        print("Plotting candidate multiplicity.")
        plot_candidate_multiplicity(data, out_dir_path)
    
    if "generics" in plots:
        print("Plotting generics.")
        info = generate_plot_info(
            variables = ["costheta_K", "costheta_mu", "chi", "q_squared"],
            xlabels = [r"", r"", r"", r"GeV$^2$"],
            titles = [r"$\cos\theta_K$", r"$\cos\theta_\mu$", r"$\chi$", r"$q^2$"],
            q_squared_splits = ["all", "med"],
        )

        for variable, xlabel, title, q_squared_split in info:
            plot_gen_det_compare(
                data,
                variable=variable,
                q_squared_split=q_squared_split, 
                title=title,
                xlabel=xlabel,
                out_dir_path=out_dir_path
            )    

    if "helicity vs p theta" in plots:
        print("Plotting helicity angle vs. lab momentum and lab theta.")

        plot_hel_p_theta()

