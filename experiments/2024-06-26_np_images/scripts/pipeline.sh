
# Create a completed image file (and log file).
# NOTES: 
#    Only works for ell = mu (for now).
#    Requires Alexei's basf2 env (and my python library).


simulate() {
    local dc9_real=$1
    local trial=$2
    local n_events=$3
    
    basf2 mc_gen_steer.py -- $dc9_real $trial $n_events &>> $path_log
    
    echo "$(bash image_name.sh $dc9_real $trial).root"
}


basic_recon() {
    local ell=$1
    local file_in=$2
    
    local file_out="${file_in%.root}_re.root"
    local file_log="${file_in%.root}.log"
    
    basf2 recon.py $ell $file_in $file_out &>> $file_log
    
    echo $file_out
}


calc_vars() {
    local ell=$1
    local file_in=$2
    
    local file_out="${file_in%.root}.pkl"
    local file_log="${file_in%_re.root}.log"
    
    python calc_vars.py $ell $file_in $file_out &>> $file_log
    
    # echo $file_out
}


ell=$1
dc9_real=$2
trial=$3
n_events=$4

file_simulate_out=$(simulate $dc9_real $trial $n_events)
file_basic_recon_out=$(basic_recon $ell $file_simulate_out)
calc_vars $ell $file_basic_recon_out
rm $file_basic_recon_out


