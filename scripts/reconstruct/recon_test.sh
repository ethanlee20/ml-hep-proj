

#in_file_names = (mc_1.root mc_2.root)
#
#for file_name in "${in_file_names[@]}"; do
#	basf2 reconstruction_steering_mu.py \
#		/home/belle2/elee20/ml-hep-proj/data/2024-01-02_recovery/ \
#		$file_name \
#		"${file_name%.*}"_rec."${file_name#*.}"
#done
#

#data_dir_path="/home/belle2/elee20/ml-hep-proj/data/2024-01-08_LargeMu_backup/"
#in_file_name="mc_1.root"
#out_file_name="mc_1_re.root"

data_dir_path="/home/belle2/elee20/ml-hep-proj/data/2024-01-08_LargeMu_backup/"
in_file_name="mc_1.root"
out_file_name="mc_1_re_test.root"

basf2 recon_steer_mu_test.py $data_dir_path $in_file_name $out_file_name
