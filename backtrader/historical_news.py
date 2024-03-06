from alpaca.common.rest import RESTClient
from alpaca.data import StockHistoricalDataClient
from alpaca.trading import TradingClient
import pandas as pd
import datetime

import os
from dotenv import load_dotenv
load_dotenv()

class DataManager(object):
    historicaldata_client: None
    trading_client:None
    rest_client:None

    def __init__(self):
        self.historicaldata_client = StockHistoricalDataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"))
        self.trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"))
        self.rest_client =RESTClient(base_url='https://data.alpaca.markets',api_version='v1beta1',api_key=os.getenv("ALPACA_API_KEY"), secret_key=os.getenv("ALPACA_SECRET_KEY"),)

    def get_news(self, symbols:pd.Series, start_datetime:datetime, end_datetime:datetime):
        utc_start_datetime = pd.to_datetime(start_datetime, utc=True)
        utc_end_datetime = pd.to_datetime(end_datetime, utc=True)
        
        news_list = []
        page_token = None
        while True:
            news_endpoint = '/news'
            parameters = {'start':utc_start_datetime.isoformat(),
                        'end':utc_end_datetime.isoformat(),
                        'page_token':page_token,
                        'symbols':symbols.to_list()
            }

            resp = self.rest_client.get(news_endpoint, parameters,)
            page_token = resp.get('next_page_token')
            temp_list = resp.get('news')
 
            news_list.extend(temp_list)
            if not page_token:
                break
            
        return news_list
    

# Create an instance of DataManager
data_manager = DataManager()

# News to retrieve. Only able to retrieve 1 stock at a time.
symbols = pd.Series(['AAPL'])

# Start and end datetime for the news retrieval
start_datetime = datetime.datetime(2023, 1, 1)
end_datetime = datetime.datetime(2023, 1, 31)

# Call the get_news method
news_list = data_manager.get_news(symbols, start_datetime, end_datetime)

print(news_list)