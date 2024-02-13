from websocket import create_connection
import json
import os
from dotenv import load_dotenv
load_dotenv()
import pprint

# TODO: Note that there is only a response when market is open. need to take this into account

# real-time stock data
# uri = 'wss://stream.data.alpaca.markets/v2/iex'

# real-time crypto data
uri = 'wss://stream.data.alpaca.markets/v1beta3/crypto/us'

ws = create_connection(uri)

auth_message = {"action":"auth","key": os.getenv("ALPACA_API_KEY"), "secret": os.getenv("ALPACA_SECRET_KEY")}
ws.send(json.dumps(auth_message))

# stock
# subscription = {"action":"subscribe","trades":["VV"],"quotes":["VV"],"bars":["VV"]}

# crypto
# TODO: understand all these things mean
subscription = {"action":"subscribe","trades":["BTC/USD"],"quotes":["LTC/USD","ETH/USD"],"bars":["BCH/USD"]}

ws.send(json.dumps(subscription))
while True:
    data = json.loads(ws.recv())
    pprint.pprint(data[0])
    print('****************************')
    exit