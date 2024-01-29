
import pathlib as pl

import mylib


def main():
    mylib.setup_mpl_params_save()

    plots_dir_path = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/plots/')
    plots_dir_path.mkdir(exist_ok=True)


#    data = mylib.open('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/mu_re_00016_job388070885_00_cut_an.pkl')
    data = mylib.open_dir('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/')

    mylib.plot(
#        plots=['helicity vs p theta'],
        plots=['efficiency', 'resolution', 'candidate multiplicity', 'generics'],
#        data=mylib.open_dir('/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/'),
#        data=mylib.open('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/mu_re_00030_job386260858_00_cut_an.pkl'),
        data=data,
#        data=mylib.open_dir('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/'),
        out_dir_path=plots_dir_path,
    )    

    for split in ["all", "med"]:
        mylib.hist_2d_costheta_k_p_k(data, q_squared_split=split, out_dir=plots_dir_path)
        mylib.hist_2d_costheta_k_theta_k(data, q_squared_split=split, out_dir=plots_dir_path)

if __name__ == "__main__":
    main()
