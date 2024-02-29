impact_buy = 70    # Upper bound for long position
impact_sell = 30    # Lower bound for short position
take_profit = 1.02   # Take profit
stop_loss = 0.98    # Stop loss
# limit_price = 0.97  # Stop-limit price

account_size = 100000                               # Assume initial capital is fixed at 100,000 USD TODO: Constantly update based on account position size
position_per_trade = 0.01                           # % of account per trade
position_size = account_size * position_per_trade   # USD per trade