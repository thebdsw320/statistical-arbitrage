import json
from pybit import WebSocket

with open('./settings.json', 'r') as f:
    data = json.load(f)

ticker1 = data['ticker1']
ticker2 = data['ticker2']
ws_public_url = data['wsPublicURL']

# Public ws subscriptions
subs_public = [
    f'orderBookL2_25.{ticker1}',
    f'orderBookL2_25.{ticker2}'
]

# Public ws connection
ws_public = WebSocket(
    endpoint = ws_public_url,
    subscriptions = subs_public
)