import pandas as pd

pd.options.display.max_columns = 500

df = pd.read_pickle('../data/2023-12-8_tryingStopDoubleCandidates/mu_gen_ana.pkl')

print(df.head(6))
