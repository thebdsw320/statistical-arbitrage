# API
from pybit import HTTP, WebSocket
import json
#from os import environ

# Configuration
mode = 'test'
timeframe = 60
kline_limit = 200
z_score_window = 21

with open('../keys.json', 'r') as f:
    keys = json.load(f)

# API Main
api_key_mainnet = ... #keys['publicKey']
api_secret_mainnet = ... #keys['privateKey']

# API Test (alt. environment variables)
api_key_testnet = keys['publicKey']
api_secret_testnet = keys['privateKey']

# Credentials
api_key = api_key_testnet if mode == 'test' else api_key_mainnet
api_secret = api_secret_testnet if mode == 'test' else api_secret_mainnet

# URL
api_url = 'https://api-testnet.bybit.com' if mode == 'test' else 'https://api.bybit.com'

# Session
session = HTTP(api_url)