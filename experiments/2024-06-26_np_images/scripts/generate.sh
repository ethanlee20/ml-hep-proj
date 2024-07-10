
# Generate processed datafiles (each file represents an image) of a range
# of delta C9 values. Each delta C9 value has multiple trials (datafiles).

# Assumes basf2 environment is already setup (including my library).
# Only works for ell = mu right now.


n_events=24000

output_dir="../datafiles"

values_dc9_real=("-2.0" "-1.85" "-1.7" "-1.56" "-1.41" \
    "-1.26" "-1.11" "-0.97" "-0.82" "-0.67" "-0.52" "-0.38" \
    "-0.23" "-0.08" "0.07" "0.21" "0.36" "0.51" "0.66" "0.8" "0.95" "1.1")

trial_begin=3
trial_end=5

for dc9_real in ${values_dc9_real[@]}; do
    for ((trial=trial_begin; trial<=trial_end; trial++)); do
        bsub -q l "bash pipeline.sh mu ${dc9_real} ${trial} ${n_events} ${output_dir}"
    done
done
