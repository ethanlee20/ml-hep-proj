
# Generate processed datafiles (each file represents an image) of a range
# of delta C9 values. Each delta C9 value has multiple trials (datafiles).

# Just for reconstructing already generated MC files for now.

# Assumes basf2 environment is already setup (including my library).


n_events=24000

values_dc9_real=("-2.0" "-1.85" "-1.7" "-1.56" "-1.41" \
    "-1.26" "-1.11" "-0.97" "-0.82" "-0.67" "-0.52" "-0.38" \
    "-0.23" "-0.08" "0.07" "0.21" "0.36" "0.51" "0.66" "0.8" "0.95" "1.1")

trial_range={1..2}


image_name() {
    local dc9_real=$1
    local trial=$2
    echo "dc9_${dc9_real}_${trial}"
}


for dc9_real in ${values_dc9_real[@]}; do
    for trial in {1..2}; do
        bsub -q l "bash full_recon.sh mu ../datafiles/$(image_name $dc9_real $trial).root";
    done
done
