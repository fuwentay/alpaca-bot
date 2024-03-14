import alpaca_backtrader_api as alpaca
import backtrader as bt
import pytz
from datetime import datetime
from local_settings import alpaca_paper

ALPACA_KEY_ID = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
ALPACA_PAPER = True

fromdate = datetime(2020,8,5)
todate = datetime(2020,8,10)

tickers = ['SPY']
timeframes = {
    '15Min':15,
    '30Min':30,
    '1H':60,
}

# Creating our strategy class and initialize cerebro
# This just loads the data and prints each line for each 'next'
class RSIStack(bt.Strategy):

    def next(self):
        for i in range(0,len(self.datas)):
            print(f'{self.datas[i].datetime.datetime(ago=0)} \
            {self.datas[i].p.dataname}: OHLC: \
                  o:{self.datas[i].open[0]} \
                  h:{self.datas[i].high[0]} \
                  l:{self.datas[i].low[0]} \
                  c:{self.datas[i].close[0]} \
                  v:{self.datas[i].volume[0]}' )

cerebro = bt.Cerebro()

cerebro.addstrategy(RSIStack)
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.0)

# Add the Datastore
# A store in backtrader is the interface with a broker. 
# While the implementation for various brokers will be different, a store handles connectivity with the broker to access your account, orders, and positions; and provides access to data feeds from the broker.
store = alpaca.AlpacaStore(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER
)

if not ALPACA_PAPER:
    print(f"LIVE TRADING")
    broker = store.getbroker()
    cerebro.setbroker(broker)

DataFactory = store.getdata

for ticker in tickers:
    for timeframe, minutes in timeframes.items():
        print(f'Adding ticker {ticker} using {timeframe} timeframe at {minutes} minutes.')

        d = DataFactory(
            dataname=ticker,
            timeframe=bt.TimeFrame.Minutes,
            compression=minutes,
            fromdate=fromdate,
            todate=todate,
            historical=True)

        cerebro.adddata(d)

cerebro.run()
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.plot(style='candlestick', barup='green', bardown='red')