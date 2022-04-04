import logging
import os
import time
from datetime import datetime, timedelta

import requests
from requests.auth import HTTPBasicAuth
from dumarpc.models.dumaos_rpc_responses import get_uptime_from_system_info_response

from dumarpc.rpc_methods import create_json_log, create_request, manage_delta

log_filename='./logs/app.log'
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
logging.basicConfig(filename=log_filename, 
    level=logging.DEBUG,
    format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

def print_to_log(*args):
    logger.debug(" ".join(args))

# uncomment for enabling verbose logging for http traffic
# http.client.HTTPConnection.debuglevel = 1 
# http.client.print = print_to_log

def start(config):
    auth = HTTPBasicAuth(config['rusername'], config['rpassword'])
    base_url = 'http://' + config['router_ip']

    # login to generate auth_token for RPC requests
    response = requests.get(base_url, auth = auth)
    headers = { 'Content-Type': 'application/json-rpc' }
    auth_token = response.cookies.get('auth_token')
    cookies = { 'auth_token':  auth_token }

    interval = 1000 # ms
    timeout = 5 # seconds
    current_time = datetime.now()   
    future_time = current_time + timedelta(seconds=timeout)

    ## change this to whatever method you want to call
    method = 'filter_connections'
    params = []

    delta = manage_delta()

    f = open(f'./logs/{method}.log', 'a+')
    while (future_time > current_time):
        api_path, payload = create_request('get_system_info', [])
        url = f'{base_url}{api_path}'
        response = requests.post(url, 
            cookies = cookies, 
            headers = headers,
            auth = auth, 
            json = payload)

        content = response.content.decode("utf-8")
        print(content)
        days_up = get_uptime_from_system_info_response(content)
        date_up = datetime.today() - timedelta(days=int(days_up))
        date_up_epoch = date_up.timestamp() * 1000

        api_path, payload = create_request(method, params)
        url = f'{base_url}{api_path}' 
        response = requests.post(url, 
            cookies = cookies, 
            headers = headers,
            auth = auth, 
            json = payload)    

        log = create_json_log(response, delta, date_up_epoch)
        if (log is not None):
            f.write(log + '\n')
        time.sleep(interval / 1000)
        current_time = datetime.now()   
    f.close()

    # need uptime date ms
    # get current date is ms
    # 
