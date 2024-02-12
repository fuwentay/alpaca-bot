impact_buy = 70     # upper bound for long position
impact_sell = 30    # lower bound for short position

take_profit = 1.1   # take profit
stop_loss = 0.95    # stop loss
limit_price = 0.94  # limit price

account_size = 100000                               # assume initial capital is fixed at 100,000 USD TODO: constantly update based on account position size
position_per_trade = 0.01                           # % of account per trade
position_size = account_size * position_per_trade   # USD per trade