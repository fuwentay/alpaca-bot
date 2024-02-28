impact_buy = 75    # upper bound for long position
impact_sell = 25    # lower bound for short position # TODO: include in news_logs

take_profit = 1.02   # take profit  # TODO: include in trade_logs
stop_loss = 0.98    # stop loss
# limit_price = 0.97  # stop-limit price

account_size = 100000                               # assume initial capital is fixed at 100,000 USD TODO: constantly update based on account position size
position_per_trade = 0.01                           # % of account per trade
position_size = account_size * position_per_trade   # USD per trade