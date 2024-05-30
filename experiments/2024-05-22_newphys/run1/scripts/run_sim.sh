
for i in {1..50}; do
    bsub -q l "basf2 ../scripts/genmc_MC15ri_b.py ../scripts/B0B0bar_kstarll_sm.dec sm_$i.root"
    bsub -q l "basf2 ../scripts/genmc_MC15ri_b.py ../scripts/B0B0bar_kstarll_np.dec np_$i.root"
done
