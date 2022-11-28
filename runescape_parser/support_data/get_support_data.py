from shutil import ExecError
import pandas as pd
import os
import httpx
from runescape_parser.rs.item import Item
import numpy as np

data = httpx.get("https://prices.runescape.wiki/api/v1/osrs/mapping").json()
df = pd.json_normalize(data)
df = df.set_index('id')
breakpoint()
tradeable_col = []
for index, item in df.iterrows():
    name = item['name']
    try:
        old_item_data = Item.query_by_name(name)
    except:
        print(name)
    tradeable = old_item_data['tradeable']
    tradeable_col.append(old_item_data['tradeable'])
df['tradeable'] = tradeable_col
breakpoint()