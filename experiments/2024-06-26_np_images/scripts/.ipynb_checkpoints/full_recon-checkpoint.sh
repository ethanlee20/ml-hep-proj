
# Reconstruct an MC datafile including offline calculation of variables.
# Save result to a pandas dataframe pickle file.

# Inputs are (in this order): 
#    ell - lepton (e or mu)
#    file_in - path of input MC datafile

# Assumes basf2 environment is already activated (including personal library).
# Output file and log file will be placed in same directory as input file.
# Name of output file is 'input_file_name_re.pkl'.
# Name of log file is 'input_file_name.log'.


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
file_in=$2

file_basic_recon_out=$(basic_recon $ell $file_in)
calc_vars $ell $file_basic_recon_out
rm $file_basic_recon_out



