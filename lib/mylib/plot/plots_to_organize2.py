from math import radians
import matplotlib.pyplot as plt

from mylib.util import approx_num_bins, save_plot, section, over_q_squared_splits

from mylib.plot.core.looks.leg import stats_legend





def plot_deltaE(data, out_dir, name="deltaE_gen_det", xlim=(-0.1, 0.1)):
    fig, ax = _plot_gen_det(
        data,
        var="deltaE",
        q_squared_split=None,
        title=r'$\Delta E$',
        xlabel=r'[GeV]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_invM(data, out_dir, name="invM_gen_det", xlim=(-0.2, 0.2)):
    fig, ax = _plot_gen_det(
        data,
        var="invM_K_pi_shifted",
        q_squared_split=None,
        title=r'$M_{K, \pi} - M_{K^*}$',
        xlabel=r'[GeV]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_q_squared(data, out_dir, name="q_sq_gen_det", xlim=(0, 20)):
    fig, ax = _plot_gen_det(
        data,
        var="q_squared",
        q_squared_split=None,
        title=r'$q^2$',
        xlabel=r'[GeV$^2$]',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


def plot_tf_red_chi_sq(data, out_dir, name="tf_red_chi_sq_gen_det", xlim=(0, 10)):
    fig, ax = _plot_gen_det(
        data,
        var="tfRedChiSq",
        q_squared_split=None,
        title=r'$\chi^2_\textrm{red}$',
        xlabel=r'',
        xlim=xlim
    )
    save_plot(name, q_squared_split='all', out_dir=out_dir)


@over_q_squared_splits
def hist_chi(data, out_dir, q_squared_split):
    fig, ax = _plot_gen_det(
        data,
        var="chi",
        q_squared_split=q_squared_split,
        title=r"$\chi$",
        xlabel=None,
    )
    save_plot("chi_gen_det", q_squared_split, out_dir)


@over_q_squared_splits
def hist_costheta_e(data, out_dir, q_squared_split):
    fig, ax = _plot_gen_det(
        data,
        var="costheta_e",
        q_squared_split=q_squared_split,
        title=r"$\cos\theta_e$",
        xlabel=None,
    )
    save_plot("costheta_e_gen_det", q_squared_split, out_dir)


@over_q_squared_splits
def hist_costheta_mu(data, out_dir, q_squared_split):
    fig, ax = _plot_gen_det(
        data,
        var="costheta_mu",
        q_squared_split=q_squared_split,
        title=r"$\cos\theta_\mu$",
        xlabel=None,
    )
    save_plot("costheta_mu_gen_det", q_squared_split, out_dir)


@over_q_squared_splits
def hist_costheta_K(data, out_dir, q_squared_split):
    fig, ax = _plot_gen_det(
        data,
        var="costheta_K",
        q_squared_split=q_squared_split,
        title=r"$\cos\theta_K$",
        xlabel=None,
    )
    save_plot("costheta_K_gen_det", q_squared_split, out_dir)


@over_q_squared_splits
def hist_theta_lab_k(data, out_dir, q_squared_split):

    def make_one_scaler(min, max):
        def scale(num):
            return (num - min) / (max - min)
        return scale

    def make_big_scaler(min, max):
        def scale(num):
            return ((max - min) * num) + min
        return scale

    def annotate_theta_accept(xlim:tuple, ylim:tuple):
        one_scale = make_one_scaler(*xlim)
        big_scale = make_big_scaler(*ylim)

        plt.axhline(y=big_scale(0.1), xmin=one_scale(radians(17)), xmax=one_scale(radians(150)), label="PXD, SVD, CDC", color="red")
        plt.axhline(y=big_scale(0.2), xmin=one_scale(radians(31)), xmax=one_scale(radians(128)), label="TOP", color="aquamarine")
        plt.axhline(y=big_scale(0.3), xmin=one_scale(radians(15)), xmax=one_scale(radians(34)), label="ARICH", color="pink")
        plt.axhline(y=big_scale(0.4), xmin=one_scale(radians(12.4)), xmax=one_scale(radians(31.4)), label="ECL", color="green", linestyle="--")
        plt.axhline(y=big_scale(0.4), xmin=one_scale(radians(32.2)), xmax=one_scale(radians(128.7)), color="green", linestyle="--")
        plt.axhline(y=big_scale(0.4), xmin=one_scale(radians(130.7)), xmax=one_scale(radians(155.1)), color="green", linestyle="--")
        plt.axhline(y=big_scale(0.5), xmin=one_scale(radians(40)), xmax=one_scale(radians(129)), label="KLM", color="orange", linestyle=":")
        plt.axhline(y=big_scale(0.5), xmin=one_scale(radians(25)), xmax=one_scale(radians(40)), color="orange", linestyle=":")
        plt.axhline(y=big_scale(0.5), xmin=one_scale(radians(129)), xmax=one_scale(radians(155)), color="orange", linestyle=":")

        plt.legend()

    fig, ax = _plot_gen_det(
        data,
        var="K_p_theta",
        q_squared_split=q_squared_split,
        title=r"$\theta^\text{lab}_K$",
        xlabel=None,
    )

    annotate_theta_accept(ax.get_xlim(), ax.get_ylim())

    save_plot("theta_lab_k_gen_det", q_squared_split, out_dir)