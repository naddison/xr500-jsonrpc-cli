# Duma OS Metric Agent

This is a python CLI tool used to fetch metrics and system information from a router running Duma OS. There is no official API documentation (as of writing this README) for Duma OS, but through some devtools spleunking it was determined that the router firmware communicates to the admin interface using [json-rpc](https://www.jsonrpc.org/specification). 

Devices currently running Duma OS are listed on the [NetDuma's support page](http://support.netduma.com/support/solutions/articles/16000091217-dumaos-firmware). 

>**Note:** This client was written and tested against an Netgear XR500 router.

## Why?

This started as a weekend project of wanting to fetch simple data such as: active connections, connected devices, and in / out traffic. Instead of setting up a network tap and capture traffic using a tool like [Zeek](https://zeek.org/), I wanted to be able to fetch straight from the source. This turned into a tool I can run locally for ad-hoc use cases (testing) or automate to generate logs. Those logs then in turn could be shipped to another system for collection, such as [Elasticsearch](https://www.elastic.co/elastic-stack/), and further analysis/visualization.

# Setup

## Tech Stack
- Python 3.7+
- [SetupTools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)
    - https://github.com/navdeep-G/setup.py

## Running from source
1. Install dependencies `pip install -r requirements.txt`
2. Execute `python ./cli/__main__.py`
    - Command line arguments can be passed this was as well for example, `python ./cli/__main__.py --router-ip 192.168.1.1`

## Installing as CLI tool
1. Install dependencies `pip install -r requirements.txt`
2. Execute `./install.sh`
    - `./install.bat` for Windows machine.
3. Execute `dumarpc [command line arguments]`.

# Configuration

## Options
Configuration precedence:
1. Command Line
2. .env variables
2. Shell environment variables
3. Hardcoded defaults

|Option|CLI Flag|ENV Variable|Description|CLI Example|ENV Example
|--|--|--|--|--|--|
|router_ip|--router-ip|ROUTER_IP|ip4 address of router|--router-ip 192.168.1.1|ROUTER_IP=192.168.1.1
|rusername|--rusername|RUSERNAME|username used to login to router admin ui|--rusername admin|RUSERNAME=admin|
|rpassword|--rpassword|RPASSWORD|password used to login to router admin ui|--rpassword whee|RPASSWORD="wheeee"
