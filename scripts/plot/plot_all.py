
import pathlib as pl

import mylib


def main():
    mylib.setup_mpl_params_save()

    plots_dir_path = pl.Path('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/plots/')
    plots_dir_path.mkdir(exist_ok=True)
    
    mylib.plot(
        plots=['efficiency', 'resolution', 'candidate multiplicity', 'generics'],
        #data=mylib.open('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/mu_re_00030_job386260858_00_cut_an.pkl'),
        data=mylib.open_dir('/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/'),
        out_dir_path=plots_dir_path,
    )    


if __name__ == "__main__":
    main()
