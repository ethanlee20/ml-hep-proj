from mylib.calc.phys import calc_dif_inv_mass_k_pi_and_kst
from mylib.plot.core.util.save import save
from mylib.plot.hist_1d.sig_mis import plot_sig_mis
from mylib.plot.hist_1d.gen_det import plot_gen_det


def plot_deltaE(data, out_dir):
    fig, ax = plot_sig_mis(
        data, 
        var="deltaE", 
        title=r'$\Delta E$', 
        xlabel=r'[GeV]',
        xlim=(-0.1, 0.1)
    )
    save("deltaE_sig_mis", q_squared_split='all', out_dir=out_dir)

    fig, ax = plot_gen_det(
        data,
        var="deltaE",
        q_squared_split=None,
        title=r'$\Delta E$',
        xlabel=r'[GeV]',
        xlim=(-0.1, 0.1)
    )
    save("deltaE_gen_det", q_squared_split='all', out_dir=out_dir)


def plot_mbc(data, out_dir):
    fig, ax = plot_sig_mis(
        data,
        var="Mbc",
        title=r"$M_{bc}$",
        xlabel=r"[GeV]",
        xlim=(5.26, 5.30)
    )
    save("Mbc_sig_mis", q_squared_split='all', out_dir=out_dir)

    fig, ax = plot_gen_det(
        data,
        var="Mbc",
        q_squared_split=None,
        title=r'$M_{bc}$',
        xlabel=r'[GeV]',
        xlim=(5.26, 5.30)
    )
    save("Mbc_gen_det", q_squared_split='all', out_dir=out_dir)


def plot_invM(data, out_dir):

    fig, ax = plot_sig_mis(
        data,
        var="invM_K_pi_shifted",
        title=r"$M_{K, \pi} - M_{K^*}$",
        xlabel=r"[GeV]",
        xlim=(-0.2, 0.2)
    )
    save("invM_sig_mis", q_squared_split='all', out_dir=out_dir)

    fig, ax = plot_gen_det(
        data,
        var="invM_K_pi - invM_Kst",
        q_squared_split=None,
        title=r"$M_{K, \pi} - M_{K^*}$",
        xlabel=r'[GeV]',
        xlim=(-0.2, 0.2)
    )
    save("invM_gen_det", q_squared_split='all', out_dir=out_dir)


    