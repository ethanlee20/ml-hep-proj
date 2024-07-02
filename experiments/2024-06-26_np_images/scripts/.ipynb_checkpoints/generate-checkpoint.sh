
n_events=24000
values_dc9_real=("-2.0" "-1.85" "-1.7" "-1.56" "-1.41" \
    "-1.26" "-1.11" "-0.97" "-0.82" "-0.67" "-0.52" "-0.38" \
    "-0.23" "-0.08" "0.07" "0.21" "0.36" "0.51" "0.66" "0.8" "0.95" "1.1")
    
for dc9_real in ${values_dc9_real[@]}; do
    for trial in {1..2}; do
        path_log="../datafiles/dc9_${dc9_real}_${trial}.log";
        bsub -q l "basf2 mc_gen_steer.py -- $dc9_real $trial $n_events &>> $path_log";
    done
done