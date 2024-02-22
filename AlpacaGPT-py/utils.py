import alpaca_trade_api as api

import config
from openai import OpenAI

from websocket import create_connection
import pprint
import json

import os
from dotenv import load_dotenv
load_dotenv()

# initialise Alpaca (Rest) Client
alpaca = api.REST(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), "https://paper-api.alpaca.markets")

# bracket order that consists of market, stop and limit order
def place_bracket_order(sym, n):
    symbol_price = get_market_price(sym)    # TODO: verify that this works. shouldn't need to thread

    alpaca.submit_order(
        symbol=sym,
        qty=config.position_size/symbol_price,
        side="buy" if n == 0 else "sell",
        type='market',
        time_in_force='gtc',
        order_class='bracket',
        stop_loss={'stop_price': symbol_price * config.stop_loss,
                'limit_price':  symbol_price * config.limit_price},
        take_profit={'limit_price': symbol_price * config.take_profit}
    )

# gather impact score based on news headline
def get_impact(headline):
    client = OpenAI()

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "Only respond with a number from 1-100 detailing the impact of the headline."},
        {"role": "user", "content": "Given the headline '" + headline + "', show me a number from 1-100 detailing the impact of this headline."}
    ]
    )
    print(response.choices[0].message.content)

# obtain latest closing price for given symbol
def get_market_price(sym):
    # TODO: note that there is only a response when market is open. need to take this into account
    # TODO: can also implement uri based on stock/crypto

    uri_stock = 'wss://stream.data.alpaca.markets/v2/iex'               # real-time stock data    
    uri_crypto = 'wss://stream.data.alpaca.markets/v1beta3/crypto/us'   # real-time crypto data

    ws = create_connection(uri_crypto)

    auth_message = {"action":"auth","key": os.getenv("ALPACA_API_KEY"), "secret": os.getenv("ALPACA_SECRET_KEY")}
    ws.send(json.dumps(auth_message))

    subscription = {"action":"subscribe","bars":[sym]}  # data schema https://docs.alpaca.markets/docs/real-time-stock-pricing-data

    ws.send(json.dumps(subscription))
    while True:
        data = json.loads(ws.recv())
        if data[0]['T'] == 'b':
            close_price = data[0]['c']  # attribute "c" to return close price in 1 minute intervals
            print(close_price)
            return close_price
        else:
            pprint.pprint(data[0])
        print('****************************')
        exit