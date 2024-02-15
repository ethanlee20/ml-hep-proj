
import pathlib as pl
import matplotlib as mpl


def setup_mpl_params_save():
    mpl.rcParams["figure.figsize"] = (8, 5)
    mpl.rcParams["figure.dpi"] = 200
    mpl.rcParams["axes.titlesize"] = 28
    mpl.rcParams["figure.titlesize"] = 32
    mpl.rcParams["axes.labelsize"] = 26
    mpl.rcParams["figure.labelsize"] = 30
    mpl.rcParams["xtick.labelsize"] = 20
    mpl.rcParams["ytick.labelsize"] = 20
    mpl.rcParams["text.usetex"] = True
    mpl.rcParams[
        "text.latex.preamble"
    ] = r"\usepackage{physics}"
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.serif"] = ["Computer Modern"]


def setup_plots_dir(data_dir_path):
    data_dir_path = pl.Path(data_dir_path)
    plots_dir_path = data_dir_path.joinpath("plots")
    plots_dir_path.mkdir(exist_ok=True)
    return plots_dir_path    

