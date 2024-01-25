import sys

import mylib

#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu_backup/BtoKstMuMu/analyzed/mu_re_00030_job386260858_00_cut_an.pkl'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00000_job386260828_00.root'
#file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-17_GridMu/BtoKstMuMu/sub00/mu_re_00001_job386260829_00.root'
file_path = '/home/belle2/elee20/ml-hep-proj/scripts/reconstruct/mu_re.root'

print(file_path)

df = mylib.open(file_path, ['gen','det']) 

df_gen = df.loc['gen']
df_det = df.loc['det']
    
print('gen:\n', df_gen['mcPDG'].value_counts())
print('det:\n', df_det['mcPDG'].value_counts())

print('gen:\n', df_gen['isSignal'].value_counts())
print('det:\n', df_det['isSignal'].value_counts())

print('columns:')
print(df_gen.columns.values.tolist())

print("head: ")
print("det: ", df_det.head())
print("gen: ", df_gen.head())

print("events range: ")
print("min: ", df_gen["__event__"].min())
print("max: ", df_gen["__event__"].max())
