import backtrader as bt

# Step 1: Create a custom data loader by subclassing
class ImpactCSVData(bt.feeds.GenericCSVData):
    # Define the structure of your CSV
    lines = ('impact_score',)
    
    # Add the 'datetime' and 'impact_score' parameters to the parameter set
    params = (
        ('dtformat', '%Y/%m/%d %H:%M:%S'),  # Datetime format
        ('datetime', 0),  # Index of the datetime column in the CSV
        ('impact_score', 1),  # Index of the impact_score column in the CSV
        ('time', -1),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),        
        ('timeframe', bt.TimeFrame.Minutes),  # Timeframe (adjust accordingly)
    )

# Step 2: Load your CSV file using the custom data loader
data = ImpactCSVData(
    dataname='alpaca_backtrader/impact.csv',  # Path to your CSV file
)

# Step 3: Add the data feed to Cerebro
cerebro = bt.Cerebro()
cerebro.adddata(data)

# Add strategy, sizer, etc., as needed
# cerebro.addstrategy(YourStrategy)

# Run the backtest
cerebro.run()

# Plot the results if needed
cerebro.plot()
