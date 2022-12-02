from runescape_parser.rs.timeseries import TimeSeries, Timestep, Item
from colorama import Fore
import numpy as np

PRICE_DEVIANCE_THRESHOLD = 0.08
VOL_DEVIANCE_THRESHOLD = 0.75
VOL_MEAN_THRESHOLD = 10
HIGH_ALCH_VALUE_CUTOFF = 10
TIMESTEP = Timestep.ONE_DAY

def is_item_good_candidate(ts):
    return (ts.volume_mean > VOL_MEAN_THRESHOLD and \
           ts.volume_stddev < ts.volume_mean * VOL_DEVIANCE_THRESHOLD and \
           ts.price_stddev > ts.price_mean * PRICE_DEVIANCE_THRESHOLD and \
           np.polyfit(x=ts['timestamp'].tolist(), y=ts['meanPrice'].tolist(), deg=1)[0] > -0.000005,
           ts.price_stddev > ts.price_mean * PRICE_DEVIANCE_THRESHOLD * 1.25)

def scan():
    for item in Item.members.query(f'value > {HIGH_ALCH_VALUE_CUTOFF}')['name']:
        try:
            ts = TimeSeries.from_name(item, TIMESTEP)
            is_good_candidate, is_great_candidate = is_item_good_candidate(ts)
            if is_good_candidate:
                    color = Fore.GREEN if is_great_candidate else Fore.YELLOW
                    print(color + f"{ts.item.name}, buy limit: {ts.item.buy_limit}")
                    print(f"PRICE: mean: {ts.price_mean}, stddev: {ts.price_stddev}")
                    print(f"VOLUME: mean: {ts.volume_mean}, stddev: {ts.volume_stddev}")
                    print(f"SLOPE: {np.polyfit(x=ts['timestamp'].tolist(), y=ts['meanPrice'].tolist(), deg=1)[0]}")
                    print(ts)
                    
            else:
                print(Fore.RED + f"{ts.item.name}")
        except:
            continue

if __name__ == "__main__":
    scan()