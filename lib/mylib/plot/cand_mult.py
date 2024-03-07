
import matplotlib.pyplot as plt

from mylib.plot.core.looks.leg import stats_legend
from mylib.plot.core.util.save import save

def plot_candidate_multiplicity(data, out_dir_path):

    sig = data[data["isSignal"]==1].loc["det"]
    mis = data[data["isSignal"]==0].loc["det"]

    plt.hist(
        sig["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=stats_legend(sig["__event__"], descrp="Signal (after cuts)", show_mean=False, show_rms=False),
        color="red", 
        histtype="stepfilled"
    )
    
    plt.hist(
        mis["__event__"].value_counts().values, 
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5], 
        label=stats_legend(mis["__event__"], descrp="Misrecon. (after cuts)", show_mean=False, show_rms=False),
        color="blue", 
        histtype="step"
    )
    
    plt.title("Candidate Multiplicity")
    plt.xlabel("Candidates per Event")
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.legend()

    save(
        plot_name="cand_mult",
        q_squared_split="all",
        out_dir=out_dir_path
    )
