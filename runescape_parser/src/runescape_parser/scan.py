from runescape_parser.rs.timeseries import TimeSeries, Timestep, Item
from colorama import Fore
import numpy as np
from datetime import datetime
import pathlib
import os

PROJECT_PATH = pathlib.Path(__file__).resolve()
while PROJECT_PATH != None and PROJECT_PATH.name != "runescape_env" and PROJECT_PATH.name != '':
    PROJECT_PATH = PROJECT_PATH.parent    
SCANS_DIR = os.path.join(PROJECT_PATH, 'scans')

PRICE_DEVIANCE_THRESHOLD = 0.3
VOL_DEVIANCE_THRESHOLD = 0.5
VOL_MEAN_THRESHOLD = 10
HIGH_ALCH_VALUE_CUTOFF = 10
TIMESTEP = Timestep.ONE_DAY

SAVE_SCAN = True

def is_item_good_candidate(ts):
    return (ts.volume_mean > VOL_MEAN_THRESHOLD and \
           ts.volume_stddev < ts.volume_mean * VOL_DEVIANCE_THRESHOLD and \
           ts.price_stddev > ts.price_mean * PRICE_DEVIANCE_THRESHOLD and \
           np.polyfit(x=ts['timestamp'].tolist(), y=ts['meanPrice'].tolist(), deg=1)[0] > 0.0001, \
           ts.price_stddev > ts.price_mean * PRICE_DEVIANCE_THRESHOLD * 1.25)

def save_scan(hits):
    hits.sort(key=lambda ts: ts.potential_profit, reverse=True)
    log = f"\n\n{'='*80}\n\n".join([hit.tostring() for hit in hits])
    full_file = os.path.join(SCANS_DIR, f"{str(datetime.now())}.txt")
    with open(full_file, 'w') as file:
        file.write(log)

def scan():
    hits = []
    for item in Item.members.query(f'value > {HIGH_ALCH_VALUE_CUTOFF}')['name']:
        try:
            ts = TimeSeries.from_name(item, TIMESTEP)
            is_good_candidate, is_great_candidate = is_item_good_candidate(ts)
            if is_good_candidate:
                color = Fore.GREEN if is_great_candidate else Fore.YELLOW
                print(color + ts.tostring())
                hits.append(ts)
            else:
                print(Fore.RED + f"{ts.item.name}")
        except:
            continue
    if SAVE_SCAN:
        save_scan(hits)
    
if __name__ == "__main__":
    scan()