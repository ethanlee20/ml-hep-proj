

path_scripts="/home/belle2/elee20/ml-hep-proj/experiments/2024-05-22_newphys/run1/scripts"
path_steer="$path_scripts/genmc_MC15ri_b.py"
path_decay_sm="$path_scripts/B0B0bar_kstarll_sm.dec"
path_decay_np="$path_scripts/B0B0bar_kstarll_np.dec"


for i in {51..100}; do
    bsub -q l "basf2 $path_steer $path_decay_sm sm_$i.root"
    bsub -q l "basf2 $path_steer $path_decay_np np_$i.root"
done
