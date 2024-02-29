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
        q_squared_split='all',
        title=r'$\Delta E$',
        xlabel=r'[GeV]',
    )
    save("deltaE_gen_det", q_squared_split='all', out_dir=out_dir)