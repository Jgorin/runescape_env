import httpx
from runescape_parser.rs.timestep import Timestep

class RSApi:
    root_path = "https://prices.runescape.wiki/api/v1/osrs"
    @staticmethod
    def timeseries(item_id:int, timestep:Timestep):
        try:
            params = {"timestep":timestep.value, "id":item_id}
            res = httpx.get(f"{RSApi.root_path}/timeseries", params=params)
            return res.json()['data']
        except:
            raise Exception(f"An error occurred while fetching market stats for item {item_id}")