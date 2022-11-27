import pandas as pd
import os

dir = os.path.dirname(os.path.realpath(__file__))
df = pd.read_json(f"{dir}/items.json")
df.T.to_parquet(f"{dir}/items.parquet")