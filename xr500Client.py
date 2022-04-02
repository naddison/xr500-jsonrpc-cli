from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
username = os.getenv('XR500_USERNAME')
password = os.getenv('XR500_PASSWORD')

# blind get router homepage to get an auth_token cookie
response = requests.get('http://10.10.1.1/')
auth_token = response.cookies.get('auth_token')
print('DONE FETCHING AUTH_TOKEN: ' + auth_token)

# login using basic auth and auth token to validate the token
cookies = { "auth_token":  auth_token }
response = requests.get('http://10.10.1.1/',
    cookies = cookies,
    auth = (username, password))
print('Logged in!' + str(response.headers))

url = 'http://10.10.1.1/apps/com.netdumasoftware.ctwatch/rpc/'
rpc_methods = 'fetch_connections'
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "fetch_connections",
    "params": []
}

response = requests.post(url, cookies = cookies, json = payload)
print(response.content)