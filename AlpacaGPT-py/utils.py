# we will use alpaca_trade_api instead of alpaca
import alpaca_trade_api as api

import config
from openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()

# initialise Alpaca (Rest) Client
alpaca = api.REST(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), "https://paper-api.alpaca.markets")

# bracket order that consists of market, stop and limit order
def place_bracket_order(sym, n):
    symbol_bars = alpaca.get_barset(sym, 'minute', 1).df.iloc[0] # FIXME: doesn't fetch an accurate price
    symbol_price = symbol_bars[sym]['close']

    # We could buy a position and add a stop-loss and a take-profit of 5 %
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

# to gather impact score based on news headline
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