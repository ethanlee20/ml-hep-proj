
import matplotlib as mpl
import matplotlib.pyplot as plt


def plot_image(
    path_image_pickle_file,
    name_column_costheta_mu_bin,
    name_column_costheta_k_bin,
    name_column_chi_bin,
    name_column_q_squared,
    num_events,
):
    image = pd.read_pickle(path_image_pickle_file)
    with mpl.rc_context():
        mpl.rcParams["figure.figsize"] = (6, 5)
        mpl.rcParams["axes.titlesize"] = 28
        mpl.rcParams["axes.labelsize"] = 24

        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        sc = ax.scatter(
            image[name_column_costheta_mu_bin],
            image[name_column_costheta_k_bin],
            image[name_column_chi_bin],
            c=image[name_column_q_squared],
            cmap="magma",
        )
        ax.set_title(r"Average $q^2$ per Angular Bin")
        ax.set_xlabel(r"$\cos\theta_\mu$ Bin", labelpad=10)
        ax.set_ylabel(r"$\cos\theta_K$ Bin", labelpad=10)
        ax.set_zlabel(r"$\chi$ Bin", labelpad=10)
        ax.tick_params(pad=1)
        ax.annotate(
            f"Num. Events: {num_events}",
            (190, 250),
            xycoords="axes points",
            fontsize="xx-large",
        )
        fig.colorbar(
            sc,
            ax=ax,
            pad=0.025,
            shrink=0.6,
            location="left",
        )
