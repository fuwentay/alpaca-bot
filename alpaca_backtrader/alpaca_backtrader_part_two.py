import alpaca_backtrader_api as alpaca
import backtrader as bt
import pytz
import pandas as pd
from alpaca_backtrader.local_settings import alpaca_paper

ALPACA_KEY_ID = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
ALPACA_PAPER = True

fromdate = pd.Timestamp(2020,5,1)
todate = pd.Timestamp(2020,8,17)
timezone = pytz.timezone('US/Eastern')

tickers = ['SPY']
timeframes = {
    '15Min':15,
    '30Min':30,
    '1H':60,
}
lentimeframes = len(timeframes)

# We create our RSIStack class by inheriting all of the functionality from backtrader.strategy. 
class RSIStack(bt.Strategy):
    # We then set the parameters for our strategy in the params dictionary. 
    # The parameters dictionary is part of the Backtrader framework and makes our code more readable and maintainable.
    params = dict(
        rsi_overbought=70,
        rsi_oversold=30,
        rrr=2
    )

    # With our derived strategy class created, we can now initialize a few attributes and create our indicators in __init__. 
    # __init__ preprocesses our data to prepare it for later use, making backtesting faster.  
    # Let's create an attribute to hold our 'alive' orders and our indicators. 
    # We create our RSI indicators on every data/timeframe and only create our ATR indicator on the timeframe we're using for position sizing.
    def __init__(self):
        self.orefs = None
        self.inds = {}
        for d in self.datas:
            self.inds[d] = {}
            self.inds[d]['rsi'] = bt.ind.RSI(d)
            self.inds[d]['rsiob'] = self.inds[d]['rsi'] >= self.p.rsi_overbought
            self.inds[d]['rsios'] = self.inds[d]['rsi'] <= self.p.rsi_oversold
        for i in range(len(timeframes)-1, len(self.datas), len(timeframes)):
            self.inds[self.datas[i]]['atr'] = bt.ind.ATR(self.datas[i])

    # Start enables us to run code before next processes each bar. 
    # For our strategy, we use it to record the length of the lowest timeframe. 
    # Remember, the RSI stack requires all timeframes to be oversold or overbought. 
    # We need to reset the stack after each bar passes on the lowest timeframe.
    def start(self):
        # Timeframes must be entered from highest to lowest frequency.
        # Getting the length of the lowest frequency timeframe will
        # show us how many periods have passed
        self.lenlowtframe = len(self.datas[-1])
        self.stacks = {}

    # Determine if the period has changed by saving the length of the lowest timeframe bar and checking it against the current length of the lowest timeframe bar.
    def next(self):
        # Reset all of the stacks if a bar has passed on our
        # lowest frequency timeframe
        if not self.lenlowtframe == len(self.datas[-1]):
            self.lenlowtframe += 1
            self.stacks = {}

        # Determine if there is an RSI stack by iterating through all of the data feeds (datas) for each ticker and incrementing our stacks dictionary by one for each oversold/overbought condition. 
        # For this, we use the modulo operator and the timeframe length to determine when we're on a new ticker.
        for i, d in enumerate(self.datas):
            # Create a dictionary for each new symbol.
            ticker = d.p.dataname
            if i % len(timeframes) == 0:
                self.stacks[ticker] = {}
                self.stacks[ticker]['rsiob'] = 0
                self.stacks[ticker]['rsios'] = 0
            if i % len(timeframes) == len(timeframes) -1:
                self.stacks[ticker]['data'] = d
            self.stacks[ticker]['rsiob'] += self.inds[d]['rsiob'][0]
            self.stacks[ticker]['rsios'] += self.inds[d]['rsios'][0]

        # Delete any dictionary entry where an RSI stack isn't found.
        for k,v in list(self.stacks.items()):
            if v['rsiob'] < len(timeframes) and v['rsios'] < len(timeframes):
                del self.stacks[k]

        # Check if there are any stacks from the previous period
        # And buy/sell stocks if there are no existing positions or open orders
        positions = [d for d, pos in self.getpositions().items() if pos]
        if self.stacks and not positions and not self.orefs:
                for k,v in self.stacks.items():
                    d = v['data']
                    size = self.broker.get_cash() // d
                    if v['rsiob'] == len(timeframes) and \
                                     d.close[0] < d.close[-1]:
                        print(f"{d.p.dataname} overbought")
                        risk = d + self.inds[d]['atr'][0]
                        reward = d - self.inds[d]['atr'][0] * self.p.rrr
                        os = self.sell_bracket(data=d,
                                               price=d.close[0],
                                               size=size,
                                               stopprice=risk,
                                               limitprice=reward)
                        self.orefs = [o.ref for o in os]
                    elif v['rsios'] == len(timeframes) and d.close[0] > d.close[-1]:
                        print(f"{d.p.dataname} oversold")
                        risk = d - self.inds[d]['atr'][0]
                        reward = d + self.inds[d]['atr'][0] * self.p.rrr
                        os = self.buy_bracket(data=d,
                                              price=d.close[0],
                                              size=size,
                                              stopprice=risk,
                                              limitprice=reward)
                        self.orefs = [o.ref for o in os]


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print(f'{dt.isoformat()}: {txt}')

    def notify_trade(self, trade):
        if not trade.size:
            print(f'Trade PNL: ${trade.pnlcomm:.2f}')

    def notify_order(self, order):
        self.log(f'Order - {order.getordername()} {order.ordtypename()} {order.getstatusname()} for {order.size} shares @ ${order.price:.2f}')

        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)

cerebro = bt.Cerebro()
cerebro.addstrategy(RSIStack)
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.0)

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
