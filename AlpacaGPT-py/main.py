import websocket
import json
import utils, config

import os
from dotenv import load_dotenv
load_dotenv()

# websocket functions
def on_message(ws, message):
    print(message)
    msg = json.loads(message)
    try:
        if len(msg) > 0:
            if msg[0] and 'msg' in msg[0] and msg[0]['msg'] == 'authenticated':
                ws.send(json.dumps({"action":"subscribe","news":["*"]}))
                # Specific stock and/or crypto symbols #
                # {"action":"subscribe","news":["AAPL", "TSLA"]}
    except Exception as e:
        print(e)
        print("error with message")

    # trading strategy
    if msg[0]["T"] == "n" and len(msg[0]["symbols"]) == 1: # to ignore scenarios where 2 stocks are mentioned
        sym = msg[0]["symbols"][0]
        if utils.get_impact(msg[0]["headline"]) is not None:
            if utils.get_impact(msg[0]["headline"]) > config.impact_buy:
                utils.place_bracket_order(sym, 0)
            elif utils.get_impact(msg[0]["headline"]) < config.impact_sell:
                utils.place_bracket_order(sym, 1)
        else:
            print("Impact score is None, skipping trading action.")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    ws.send(json.dumps({"action":"auth","key":os.getenv("ALPACA_API_KEY"),"secret":os.getenv("ALPACA_SECRET_KEY")}))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.data.alpaca.markets/v1beta1/news",    # should be fetching stocks and crypto news
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()