import pathlib as pl

from mylib.plot.lib import plot_resolution, plot_sig_noise
from mylib.util import open_data, sig_


data = sig_(open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/sig/an'))
out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/plots/')


plot_sig_noise(
    data=data,
    var='q_squared',
    q_squared_split='all',
    noise_type='mis',
    title=r"$q^2$",
    xlabel="[GeV$^2$]",
    out_dir=out_dir
)

plot_resolution(
    data=data,
    variable='q_squared',
    q_squared_split='all',
    title=r"Resolution of $q^2$",
    xlabel=r"[GeV$^2$]",
    out_dir_path=out_dir
)