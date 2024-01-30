

def plot_candidate_multiplicity(data, out_dir_path):
    data_det = pre.preprocess(data, reconstruction_level="det")
    data_gen = pre.preprocess(data, reconstruction_level="gen")

    plt.hist(
        data_gen["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=generate_stats_label(data_gen["__event__"], descrp="Generator", show_mean=False, show_rms=False), 
        color="blue", 
        histtype="step"
    )

    plt.hist(
        data_det["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=generate_stats_label(data_det["__event__"], descrp="Detector (after cuts)", show_mean=False, show_rms=False),
        color="red", 
        histtype="step"
    )
    
    plt.title("Candidate Multiplicity")
    plt.xlabel("Candidates per Event")
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.legend()

    save_fig_and_clear(
        out_dir_path=out_dir_path,
        file_name="cand_mult.png",
    )
