import json
import re
from array import array
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List


@dataclass(frozen=True)
class Connection:
    timestamp: float # ms elapsed since router uptime
    sip4: str
    dip4: str
    sport: int
    dport: int
    l4proto: int
    l3proto: int
    timeout: int
    spackets: float
    dpackets: float
    sbytes: float
    dbytes: float

@dataclass(frozen=True)
class ConnectionCollection:
    timestamp: float
    connections: List[Connection]

@dataclass(frozen=True)
class FilterConnectionResponse:
    id: int
    result: List[ConnectionCollection]

@dataclass
class SystemInfo:
    uptime: str

@dataclass(frozen=True)
class SystemInfoResponse:
    id: int
    result: List[ConnectionCollection]

def connection_json_to_model(timestamp, jsondict):
    return Connection(
        timestamp,
        jsondict['sip4'],
        jsondict['dip4'],
        jsondict['sport'],
        jsondict['dport'],
        jsondict['l4proto'],
        jsondict['l3proto'],
        jsondict['timeout'],
        jsondict['spackets'],
        jsondict['dpackets'],
        jsondict['sbytes'],
        jsondict['dbytes']
    )

def deserialize_filter_connection_response(jsonstr):
    models = []
    results = json.loads(jsonstr)['result']
    for result in results:
        timestamp = result['timestamp']
        connections = result['connections']
        for connection in connections:
            models.append(connection_json_to_model(timestamp, connection))
    return models
    
def get_uptime_from_system_info_response(jsonstr):
    system_info = json.loads(jsonstr)
    p = re.compile("up (\\d+) days,(.+), load")
    m = p.search(system_info['result'][0]['uptime'])
    if m is not None:
        days_up = m.group(1)
        time_up = m.group(2)
        millis_up = int(days_up) * 24 * 60 * 60 * 1000 # first group is days
        if 'min' in time_up: # sometimes response gives "X min" as uptime
            minutes = time_up.replace('min').strip()
            millis_up += int(minutes) * 60 * 1000
        else: # format usually in HH:MM
            time_up = time_up.split(':')
            hours = time_up[0].strip()
            minutes = time_up[1].strip()
            millis_up += int(hours) * 60 * 60 * 1000
            millis_up += int(minutes) * 60 * 1000
        date_up = datetime.today() - timedelta(milliseconds=int(millis_up))
        return date_up.timestamp() * 1000
