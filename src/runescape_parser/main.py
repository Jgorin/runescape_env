from rs.timeseries import TimeSeries, Timestep, Item
from colorama import Fore

for item in Item.tradeable_members.query('value > 100')['name']:
    try:
        ts = TimeSeries.from_name(item, Timestep.ONE_DAY)
        if ts.score > 8:
            print(Fore.GREEN + f"{ts.item.name}: {ts.score}")
            print(Fore.GREEN + f"PRICE: mean: {ts.price_mean}, stddev: {ts.price_stddev}")
            print(Fore.GREEN + f"VOLUME: mean: {ts.volume_mean}, stddev: {ts.volume_stddev}")
            print(ts)
        else:
            print(Fore.RED + f"{ts.item.name}: {ts.score}")
    except:
        continue
