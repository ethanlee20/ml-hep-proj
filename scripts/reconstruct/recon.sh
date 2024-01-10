

#in_file_names = (mc_1.root mc_2.root)
#
#for file_name in "${in_file_names[@]}"; do
#	basf2 reconstruction_steering_mu.py \
#		/home/belle2/elee20/ml-hep-proj/data/2024-01-02_recovery/ \
#		$file_name \
#		"${file_name%.*}"_rec."${file_name#*.}"
#done
#

#data_dir_path="/home/belle2/elee20/ml-hep-proj/data/2024-01-02_recovery_backup/"
#in_file_name="mc_events_mu.root"
#out_file_name="re_test.root"


data_dir_path="/home/belle2/elee20/ml-hep-proj/data/2024-01-08_LargeMu_backup/"
out_file_name="mc_re.root"
in_file_names=(mc_1.root mc_2.root mc_3.root mc_4.root mc_5.root mc_6.root mc_7.root mc_8.root mc_9.root mc_10.root)
#in_file_names=(mc_1.root mc_2.root mc_3.root)

basf2 recon_steer_mu.py $data_dir_path $out_file_name ${in_file_names[@]}
