from dataclasses import dataclass

@dataclass
class TotalActivity: 
    timestamp: float
    in_bytes: float
    out_bytes: float
    
@dataclass
class IntervalTotalActivity:
    t1: float
    t2: float
    time_delta_ms: float
    in_bytes: float
    out_bytes: float
