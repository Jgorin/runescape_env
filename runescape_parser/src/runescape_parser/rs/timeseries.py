import pandas as pd
import numpy as np
from runescape_parser.rs.item import Item
from runescape_parser.rs.api_wrapper import RSApi
from runescape_parser.rs.timestep import Timestep

class TimeSeries(pd.DataFrame):
    def __init__(self, item:Item, timestep:Timestep):
        timeline_data = RSApi.timeseries(item.id, timestep)
        dataframe = pd.json_normalize(timeline_data)
        super().__init__(columns=dataframe.columns, index=dataframe.index, data=dataframe.values)
        self.item = item
        self.timestep = timestep
        self.insert_mean_column(['avgLowPrice','avgHighPrice'], 'meanPrice')
        self.insert_mean_column(['lowPriceVolume','highPriceVolume'], 'meanVolume')
        self.price_mean = self['meanPrice'].mean()
        self.volume_mean = self['meanVolume'].mean()
        self.price_stddev = self['meanPrice'].std()
        self.volume_stddev = self['meanVolume'].std()
        self.potential_profit = self.item.buy_limit * self.price_stddev

    def insert_mean_column(self, col_names, name):
        """
        adds a new column containing the mean values of col_names
        """
        cols = self.columns.to_list()
        index = max([cols.index(col) for col in col_names]) + 1
        mean = self[col_names].mean(axis=1)
        self.insert(index, name, mean)
    
    def segment(self, col_names, segments=25):
        """
        splits dataframe into number of segments
        """
        length = self.shape[0]
        res = []
        segment_length = round(length/segments)
        for i in range(0, length, segment_length):
            res.append(self[col_names].iloc[i:i+segment_length-1])
        return np.array(res, dtype=object)
    
    def tostring(self, print_data=True):
        res = f"{self.item.name}, buy limit: {self.item.buy_limit}, POTENTIAL PROFIT: {self.potential_profit}\n"
        res += f"PRICE: mean: {self.price_mean}, stddev: {self.price_stddev}\n"
        res += f"VOLUME: mean: {self.volume_mean}, stddev: {self.volume_stddev}\n"
        res += f"SLOPE: {np.polyfit(x=self['timestamp'].tolist(), y=self['meanPrice'].tolist(), deg=1)[0]}"
        if print_data:
            res += str(self.iloc[:4].append(self.iloc[-4:]))
        return res

    @staticmethod
    def from_name(name:str, timestep:Timestep):
        return TimeSeries(Item(name), timestep)