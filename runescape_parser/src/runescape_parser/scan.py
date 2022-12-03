from runescape_parser.rs.timeseries import TimeSeries, Timestep, Item
from colorama import Fore
import numpy as np
from datetime import datetime
from runescape_parser.utils import resolve_path
import os
import yaml

PROJECT_PATH = resolve_path(__file__, 'runescape_env')
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
SAVE_PATH = os.path.join(PROJECT_PATH, 'scans')
CONFIG_PATH = os.path.join(SCRIPT_PATH, "config.yaml")

TIMESTEP = Timestep.ONE_DAY
CONFIG = yaml.safe_load(open(CONFIG_PATH))
TIMESTEP_CONFIG = CONFIG[TIMESTEP.name]
assert CONFIG['stdout'] == True or CONFIG['save'] == True, "Either stdout or save must be true, but both are set to false."

def is_item_good_candidate(ts):
    return (ts.volume_mean > TIMESTEP_CONFIG['vol_mean_threshold'] and \
           ts.volume_stddev < ts.volume_mean * TIMESTEP_CONFIG['vol_deviance_threshold'] and \
           ts.price_stddev > ts.price_mean * TIMESTEP_CONFIG['price_deviance_threshold'] and \
           np.polyfit(x=ts['timestamp'].tolist(), y=ts['meanPrice'].tolist(), deg=1)[0] > TIMESTEP_CONFIG['linear_fit_slope_threshold'], \
           ts.price_stddev > ts.price_mean * TIMESTEP_CONFIG['price_deviance_threshold'] * TIMESTEP_CONFIG['great_threshold'])

def save_scan(hits):
    hits.sort(key=lambda ts: ts.potential_profit, reverse=True)
    log = f"\n\n{'='*80}\n\n".join([hit.tostring() for hit in hits])
    full_file = os.path.join(SAVE_PATH, f"{str(datetime.now())}.txt")
    with open(full_file, 'w') as file:
        file.write(log)

def scan():
    hits = []
    for item in Item.members.query(f'value > {TIMESTEP_CONFIG["high_alch_threshold"]}')['name']:
        try:
            ts = TimeSeries.from_name(item, TIMESTEP)
            is_good_candidate, is_great_candidate = is_item_good_candidate(ts)
            if is_good_candidate:
                hits.append(ts)
                if CONFIG['stdout']:
                    color = Fore.GREEN if is_great_candidate else Fore.YELLOW
                    print(color + ts.tostring())
            else:
                if CONFIG['stdout']:
                    print(Fore.RED + f"{ts.item.name}")
        except:
            continue
    if CONFIG['save']:
        save_scan(hits)
    
if __name__ == "__main__":
    scan()