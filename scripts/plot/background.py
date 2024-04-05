

from mylib.plot.lib import setup_mpl_params_save
from mylib.util import open_data


setup_mpl_params_save()


data_gen_mix_mc = (open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/mixed/an')).loc["det"][:20_000]
data_sig_mc = (open_data('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/sig/an')).loc["det"][:20_000]

data = pd.concat([data_bkg_mix, data_sig])

data = veto_q_squared(data)

out_dir = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-03-20_bdt_dataset/plots/')

# plot_deltaE(data, out_dir)
# plot_invM(data, out_dir)
# plot_Mbc(data, out_dir)
# plot_q_squared(data, out_dir, xlim=(0,20), name="q_sq_all")
# plot_q_squared(data, out_dir, xlim=(7,12), name="q_sq_jpsi")
# plot_q_squared(data, out_dir, xlim=(11,18), name="q_sq_psi2s")
plot_tf_red_chi_squared(data, out_dir, xlim=(0,50))