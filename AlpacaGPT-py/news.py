import websocket
import json
import utils, database

import os
from dotenv import load_dotenv
load_dotenv()

# To log all news through Alpaca news websocket onto database
def on_message(ws, message):
    print(message)
    msg = json.loads(message)
    try:
        if len(msg) > 0:
            if msg[0] and 'msg' in msg[0] and msg[0]['msg'] == 'authenticated':
                ws.send(json.dumps({"action":"subscribe","news":["*"]}))
    except Exception as e:
        print(e)
        print("error with message")

    # log to "news only" table
    if msg[0]["T"] == "n":
        sym = msg[0]["symbols"][0]
        headline = msg[0]["headline"]
        impact = utils.get_impact(headline)
        database.log_news_only(
            sym = sym,
            headline = headline,
            impact = impact
        )

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    ws.send(json.dumps({"action":"auth","key":os.getenv("ALPACA_API_KEY"),"secret":os.getenv("ALPACA_SECRET_KEY")}))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.data.alpaca.markets/v1beta1/news",    # fetches both stocks and crypto news
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()