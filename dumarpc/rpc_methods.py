
import dataclasses
import json
import re

from dumarpc.models.derived import IntervalTotalActivity, TotalActivity
from dumarpc.models.dumaos_rpc_responses import \
    deserialize_filter_connection_response

api_urls = [
    '/apps/com.netdumasoftware.systeminfo/rpc/',
    '/apps/com.netdumasoftware.procmanager/rpc/',
    '/apps/com.netdumasoftware.ctwatch/rpc/',
    '/apps/com.netdumasoftware.desktop/rpc/',
    '/apps/com.netdumasoftware.devicemanager/rpc/'
]

# timestamps are ms since uptime
methods = {
    "filter_connections": {
        "api_url": api_urls[2]
    },
    "get_all_devices": {
        "api_url": api_urls[4]
    },
    "get_arl_table": {
        "api_url": api_urls[4]
    },
    "get_cpu_info": {
        "api_url": api_urls[0]
    },
    "get_flash_info": {
        "api_url": api_urls[0]
    },
    "get_network_statistics": {
        "api_url": api_urls[0]
    },
    "get_ram_info": {
        "api_url": api_urls[0]
    },
    "get_switch_port_states": {
        "api_url": api_urls[4]
    },
    "get_system_info": {
        "api_url": api_urls[0]
    },
    "get_valid_online_interfaces": {
        "api_url": api_urls[4]
    },
    "installed_rapps": {
        "api_url": api_urls[1]
    },
    "rapp_diskusage": {
        "api_url": api_urls[1]
    },
    "read_log": {
        "api_url": api_urls[0]
    }
}

# https://stackoverflow.com/a/51286749
class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

def create_request(method, params): 
    if method not in methods.keys():
        raise ValueError(f'{method} is an unknown method.')
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": f'{method}',
        "params": params
    }
    return (methods[method]["api_url"], payload)

def manage_delta():
    previous = None
    def calcuate_delta(current: TotalActivity):
        nonlocal previous
        if (previous is None) or (previous.timestamp == current.timestamp):
            previous = current
            return
        delta_ms = current.timestamp - previous.timestamp
        delta_in_bytes = current.in_bytes - previous.in_bytes
        delta_out_bytes = current.out_bytes - previous.out_bytes
        calculated_delta = IntervalTotalActivity(
            previous.timestamp, 
            current.timestamp,
            delta_ms,
            delta_in_bytes,
            delta_out_bytes)
        previous = current
        return calculated_delta
    return calcuate_delta

def create_json_log(response, delta, uptime_epoch):
    models = deserialize_filter_connection_response(response.content.decode("utf-8"))
    total_in = 0
    total_out = 0
    for connection in models:
        total_out += connection.sbytes
        total_in += connection.dbytes
    total_activity = TotalActivity(round(uptime_epoch + models[0].timestamp), total_in, total_out)
    calculated_delta = delta(total_activity)
    if (calculated_delta is not None):
        return json.dumps(calculated_delta, cls=EnhancedJSONEncoder)
    else:
        return None    
