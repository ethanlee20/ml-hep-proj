
import mylib as my


def plot(data, plots_dir_path):
    my.hist_2d_costheta_k(
        data=data, 
        out_dir=plots_dir_path
    )
    

def main():
    data, plots_dir_path = my.setup_plotting(
        data_path='/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/analyzed/',
        plots_dir_path='/home/belle2/elee20/ml-hep-proj/data/2024-01-24_GridMu/BtoKstMuMu_theta/plots/'
    )
    plot(
        data=data, 
        plots_dir_path=plots_dir_path
    )


if __name__ == "__main__":
    main()


