import pandas as pd
import os

DIR = os.path.dirname(os.path.realpath(__file__))
ITEMS_DATA_PATH = f"{DIR}/support_data/items.parquet"
ITEMS_DATA = pd.read_parquet(ITEMS_DATA_PATH)

class Item:    
    tradeable = ITEMS_DATA.query('tradeable == True')
    members = ITEMS_DATA.query('members == True')
    f2p = ITEMS_DATA.query('members == False')
    tradeable_members = ITEMS_DATA.query('members == True and tradeable == True')
    tradeable_f2p = ITEMS_DATA.query('members == False and tradeable == True')
    
    def __init__(self, name:str):
        self.data = Item.query_by_name(name)
        self.name = self.data['name']
        self.id = self.data.name
        
    @staticmethod
    def name2id(name:str):
        return Item.query_by_name(name).name
    
    @staticmethod
    def query_by_name(name):
        return ITEMS_DATA.query('name.str.lower() == @name.lower()').iloc[0]
