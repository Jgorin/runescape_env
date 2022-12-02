from runescape_parser.rs.timeseries import TimeSeries, Timestep, Item
from colorama import Fore
import numpy as np
from datetime import datetime
import pathlib
import os

PROJECT_PATH = pathlib.Path(__file__).resolve()
breakpoint()
while PROJECT_PATH != None and PROJECT_PATH.name != "runescape_env" and PROJECT_PATH.name != '':
    PROJECT_PATH = PROJECT_PATH.parent
    
SCANS_DIR = os.path.join(PROJECT_PATH, 'scans')

# PRICE_DEVIANCE_THRESHOLD = 0.25
# VOL_DEVIANCE_THRESHOLD = 0.5
# VOL_MEAN_THRESHOLD = 10
# HIGH_ALCH_VALUE_CUTOFF = 10
# TIMESTEP = Timestep.ONE_DAY

PRICE_DEVIANCE_THRESHOLD = 0
VOL_DEVIANCE_THRESHOLD = 3
VOL_MEAN_THRESHOLD = 0
HIGH_ALCH_VALUE_CUTOFF = 1
TIMESTEP = Timestep.ONE_DAY

def is_item_good_candidate(ts):
    return (ts.volume_mean > VOL_MEAN_THRESHOLD and \
           ts.volume_stddev < ts.volume_mean * VOL_DEVIANCE_THRESHOLD and \
           ts.price_stddev > ts.price_mean * PRICE_DEVIANCE_THRESHOLD and \
           np.polyfit(x=ts['timestamp'].tolist(), y=ts['meanPrice'].tolist(), deg=1)[0] > -5, \
           ts.price_stddev > ts.price_mean * PRICE_DEVIANCE_THRESHOLD * 1.25)

def save_scan(hits):
    hits.sort(key=lambda ts: ts.potential_profit, reverse=True)
    log = f"\n\n{'='*50}\n\n".join([hit.tostring() for hit in hits])
    full_file = os.path.join(SCANS_DIR, f"{str(datetime.now())}.txt")
    breakpoint()
    with open(full_file, 'w') as file:
        file.write(log)

def scan():
    hits = []
    for item in Item.members.query(f'value > {HIGH_ALCH_VALUE_CUTOFF}')[:5]['name']:
        try:
            ts = TimeSeries.from_name(item, TIMESTEP)
            is_good_candidate, is_great_candidate = is_item_good_candidate(ts)
            if is_good_candidate:
                    color = Fore.GREEN if is_great_candidate else Fore.YELLOW
                    print(color + ts.tostring())
            else:
                print(Fore.RED + f"{ts.item.name}")
        except:
            continue
    save_scan(hits)
    
if __name__ == "__main__":
    scan()