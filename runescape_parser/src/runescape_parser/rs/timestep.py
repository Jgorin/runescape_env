from enum import Enum

class Timestep(Enum):
    FIVE_MIN = "5m"
    TEN_MIN = "10m"
    THIRTY_MIN = "30m"
    ONE_HOUR = "1h"
    ONE_DAY = "24h"