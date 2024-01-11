import sys

import mylib

file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-08_LargeMu_backup/mc_re_cut.pkl'

df = mylib.open(file_path, ['gen','det']) 

print('test:\n', df['mcE'])

df_gen = df.loc['gen']
df_det = df.loc['det']
    
print('gen:\n', df_gen['mcPDG'].value_counts())
print('det:\n', df_det['mcPDG'].value_counts())


def print_issignal_counts():
    print('gen:\n', df_gen['isSignal'].value_counts())
    print('det:\n', df_det['isSignal'].value_counts())
print_issignal_counts()

def print_columns():
    print('columns:')
    print(df_gen.columns.values.tolist())

#print_columns()
