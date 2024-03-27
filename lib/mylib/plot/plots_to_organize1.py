
import matplotlib.pyplot as plt

from mylib.plot.core.looks.leg import stats_legend
from mylib.plot.lib import plot_sig_noise
from mylib.util import save_plot
from mylib.util import (
    approx_num_bins,
    sig_,
    noise_
)





def plot_deltaE(data, noise_type, out_dir, name="deltaE_sig_noise", xlim=(-0.1,0.1)):
    fig, ax = plot_sig_noise(
        data, 
        var="deltaE", 
        noise_type=noise_type,
        title=r'$\Delta E$', 
        xlabel=r'[GeV]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_Mbc(data, noise_type, out_dir, name="Mbc_sig_noise", xlim=(5.26, 5.30)):
    fig, ax = plot_sig_noise(
        data, 
        var="Mbc",
        noise_type=noise_type,
        title=r"$M_{bc}$",
        xlabel=r'[GeV]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_invM(data, noise_type, out_dir, name="invM_sig_noise", xlim=(-0.2, 0.2)):
    fig, ax = plot_sig_noise(
        data, 
        var="invM_K_pi_shifted",
        noise_type=noise_type,
        title=r"$M_{K, \pi} - M_{K^*}$",
        xlabel=r'[GeV]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_q_squared(data, noise_type, out_dir, name="q_sq_sig_noise", xlim=(0,20)):
    fig, ax = plot_sig_noise(
        data, 
        var="q_squared",
        noise_type=noise_type,
        title=r"$q^2$",
        xlabel=r'[GeV$^2$]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_tf_red_chi_sq(data, noise_type, out_dir, name="tf_red_chi_sq_sig_noise", xlim=(0,10)):
    fig, ax = plot_sig_noise(
        data, 
        var="tfRedChiSq",
        noise_type=noise_type,
        title=r"$\chi^2_\textrm{red}$",
        xlabel=r"",
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)



