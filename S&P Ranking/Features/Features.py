import math
from sklearn.model_selection import train_test_split
from statistics import mean
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale
import pandas as pd
import numpy as np

# replace keys to use
from paperconfig import api_key2, secret_key2
from config import api_key, secret_key

from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

class getData:

    def __init__(self,symbols):

        timeFrame = TimeFrame.Minute
        start = (date.today() - relativedelta(weeks=1)).strftime("%Y-%m-%d")
        end = (date.today()- relativedelta(days=1)).strftime("%Y-%m-%d")
        api = REST(api_key, secret_key)

        self.table = api.get_bars(symbols, timeFrame, start, end, adjustment='raw').df


class rankPortfolio:

    def __init__(self,data):
        scores = []
        test = pd.DataFrame(data)
        test = test['symbol'].drop_duplicates()
        for symbol in test:
            symbol_data = data.loc[data['symbol'] == symbol]
            symbol_data = symbol_data[['open','high','low','close','volume']]
            symbol_data.fillna(value=-99999,inplace=True)
            forecast_col = 'close'
            forecast_out = int(math.ceil(0.01 * len(symbol_data)))
            symbol_data['label'] = symbol_data[forecast_col].shift(-forecast_out)
            symbol_data.dropna(inplace=True)

            X = symbol_data.iloc[:,:-1]
            y = symbol_data.label
            
            X_scaled =scale(X)
            X_scaled = pd.DataFrame(X_scaled)

            X_train,X_test,y_train,y_test = train_test_split(X_scaled,y)
            model = LinearRegression()
            model.fit(X_train,y_train)
            y_predict = model.predict(X_test)
            pred = mean(y_predict)

            denom = symbol_data['close']
            prediction = pred/denom[0]



            scores.append(prediction)
        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset=['symbol'],keep='last')
        df = df.drop(columns=['open','high','low','trade_count','vwap'])
        df['scores'] = scores
        df = df.sort_values(by='scores',ascending=False)
        df = df.reset_index()
        df = df.drop(columns='timestamp')
        self.table = df

class getSpSymbols:
    def __init__(self):
        sptickers = []
        sp = pd.read_html('https://stockmarketmba.com/stocksinthesp500.php')

        for x in sp:
            string =  (x['Symbol'])
            for y in string:
                sptickers.append(y)
        sptickers.remove('TOTAL')

        self.table = sptickers

class buyOrder:
    def __init__(self,symbol):
        trading_client = TradingClient(api_key2, secret_key2)
        order_data = MarketOrderRequest(symbol=symbol, qty=1000, side=OrderSide.BUY, time_in_force=TimeInForce.DAY)
        trading_client.submit_order(order_data=order_data)
        print ('Bought:',symbol)
