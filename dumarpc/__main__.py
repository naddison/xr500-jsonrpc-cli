import argparse
import os

from dotenv import load_dotenv
from dumaos_client import start

load_dotenv(override=True)

def is_option_set(option):
    if option is not None:
        if isinstance(option, str):
            return True if (len(option) > 0) else False
        else:
            return True
    return False

def determine_option(option, args_dict, default = ''):
    try:
        arg_option = args_dict[option]
    except KeyError:
        arg_option = None
    env_option = os.getenv(option.upper(), '')
    if is_option_set(arg_option):
        return arg_option
    elif is_option_set(env_option):
        return env_option
    else:
        return default

def main():
    parser = argparse.ArgumentParser(
        prog='DumaOS Metric Fetcher',
        description='DumaOS router metrics fetcher script thing')
    parser.add_argument('--router_ip', help='ip4 address of router')
    parser.add_argument('--rusername', help='username credential for router')
    parser.add_argument('--rpassword', help='password credential for router')
    args = parser.parse_args()

    config = {
        'rusername': '',
        'rpassword': '',
        'router_ip': ''
    }

    errorVars = []
    for key in config.keys():
        config[key] = determine_option(key, vars(args))
        if not len(config[key]):
            errorVars.append(key)
    if len(errorVars):
        raise ValueError(f'Missing config values for: {errorVars}.')

    start(config)

if __name__ == '__main__':
    main()