import backtrader as bt
import pandas as pd
import yfinance as yf

aapl_localised_csv_parsed = bt.feeds.GenericCSVData(
    dataname='alpaca_backtrader/aapl_localised.csv',
    datetime=0,
    open=1,
    high=2,
    low=3,
    close=5,
    volume=6,
    openinterest=-1,
    dtformat='%Y-%m-%d %H:%M:%S',
    timeframe=bt.TimeFrame.Minutes
)

cerebro = bt.Cerebro()

cerebro.adddata(aapl_localised_csv_parsed)

cerebro.run()
cerebro.plot(iplot=False)