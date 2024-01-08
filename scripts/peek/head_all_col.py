import pandas as pd
import util

df = util.open_tree(
    "../data/2023-12-8_tryingStopDoubleCandidates/mc_events_mu_reconstructed.root:det"
)


pd.options.display.max_columns = 500
print(df.head(6))
