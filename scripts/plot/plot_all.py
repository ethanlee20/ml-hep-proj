
import pathlib as pl


import mylib



def plot_comp(data, plots_dir_path):

    for q_squared_split in ['all', 'med']:

        mylib.plot_gen_det_compare(
            variable='costheta_K',
            data=data[data["isSignal"]==1],
            q_squared_split=q_squared_split,
            title=r'Comparison of $\cos\theta_K$',
            xlabel=r'',
            out_dir_path=plots_dir_path
        )
        
        mylib.plot_gen_det_compare(
            variable='costheta_mu',
            data=data[data["isSignal"]==1],
            q_squared_split=q_squared_split,
            title=r'Comparison of $\cos\theta_\mu$',
            xlabel='',
            out_dir_path=plots_dir_path
        )
        
        mylib.plot_gen_det_compare(
            variable='chi',
            data=data[data["isSignal"]==1],
            q_squared_split=q_squared_split,
            title=r'Comparison of $\chi$',
            xlabel='',
            radians=True,
            out_dir_path=plots_dir_path
        )

        mylib.plot_gen_det_compare(
            variable='q_squared',
            data=data[data["isSignal"]==1],
            q_squared_split=q_squared_split,
            title=r'Comparison of $q^2$',
            xlabel='GeV$^2$',
            out_dir_path=plots_dir_path
        )


def plot_eff(data, plots_dir_path):

    num_data_points = 20
    
    for q_squared_split in ["all","med"]:
        mylib.plot_efficiency(
            data=data,
            variable="costheta_mu", 
            q_squared_split=q_squared_split,
            num_data_points=num_data_points,
            title=r"Efficiency for $\cos\theta_\mu$",
            xlabel=r"$\cos\theta_\mu$",
            out_dir_path=plots_dir_path
        )

        mylib.plot_efficiency(
            data=data,
            variable="costheta_K", 
            q_squared_split=q_squared_split,
            num_data_points=num_data_points,
            title=r"Efficiency for $\cos\theta_K$",
            xlabel=r"$\cos\theta_K$",
            out_dir_path=plots_dir_path
        )

        mylib.plot_efficiency(
            data=data,
            variable="chi", 
            q_squared_split=q_squared_split,
            num_data_points=num_data_points,
            title=r"Efficiency for $\chi$",
            xlabel=r"$\chi$",
            radians=True,
            out_dir_path=plots_dir_path
        )


def plot_res(data, plots_dir_path):

    mylib.plot_resolution(
        vars=['costheta_mu', 'costheta_K', 'chi'], 
        q_squared_splits=['all', 'med'],
        data=data,
        out_dir_path=plots_dir_path,
    )


def main():
    mylib.setup_mpl_params_save()
    
    data = mylib.open_dir('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/')
    plots_dir_path = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/plots/')
    plots_dir_path.mkdir(exist_ok=True)

#    plot_comp(data, plots_dir_path)
    plot_eff(data, plots_dir_path)
    plot_res(data, plots_dir_path)



if __name__ == "__main__":
    main()
