import sys

import mylib

file_path = '/home/belle2/elee20/ml-hep-proj/data/2024-01-08_LargeMu_backup/mc_re.root'

df = mylib.open_root(file_path, ["gen", "det"])

print('gen:\n', df.loc['gen'])
print('det:\n', df.loc['det'])
