import pandas as pd
import os

DIR = os.path.dirname(os.path.realpath(__file__))
ITEMS_DATA_PATH = f"{'/'.join(DIR.split('/')[:-3])}/support_data/items_data.parquet"
ITEMS_DATA = pd.read_parquet(ITEMS_DATA_PATH)

class Item:    
    members = ITEMS_DATA.query('members == True')
    f2p = ITEMS_DATA.query('members == False')
    
    def __init__(self, name:str):
        self.data = Item.query_by_name(name)
        self.members = self.data['members']
        self.buy_limit = self.data['limit']
        self.name = self.data['name']
        self.id = self.data.name
        
    @staticmethod
    def name2id(name:str):
        return Item.query_by_name(name).name
    
    @staticmethod
    def query_by_name(name):
        return ITEMS_DATA.query('name.str.lower() == @name.lower()').iloc[0]
