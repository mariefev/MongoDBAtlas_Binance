# command line to get seasonal decompose of historical BTCEUR data :
# python3 .\historical_data_Binance_load_print_Time_Series_v3.py

#install librairies requests and statsmodels 
#pip install requests
#cf. https://www.statsmodels.org/dev/install.html
#python3 -m pip install statsmodels

import requests
import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# Binance API used to get historical data
url = 'https://api.binance.com/api/v3/klines'

# Param to get chosen data
year_1 = 2021
year_2 = 2023
start_period = str(int(dt.datetime(year_1,1,1).timestamp()*1000)) # start date period
end_period = str(int(dt.datetime(year_2,9,1).timestamp()*1000)) # end date period
symbol = 'BTCEUR' # crypto market
interval = '1d' # interval between records 1d = 1 day

par = {'symbol': symbol, 'interval': interval, 'startTime': start_period, 'endTime': end_period}

# API Request
data_dict= json.loads(requests.get(url, params=par).text)
with open("historical_KLine_data_dict.json", "w") as historical_KLine_data_dict:
    json.dump(data_dict, historical_KLine_data_dict)

data_df=pd.DataFrame(data_dict)

# DataFrame tuning
data_df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'nbr_trades','taker_base_vol', 'taker_quote_vol', 'unused_field']
data_df.index = [dt.datetime.fromtimestamp(d/1000.0) for d in data_df.datetime]
data_df.sort_index()
data_df=data_df.astype(float)

# DataFrame head (10)
print(data_df.head(10))

# Chart
data_df["open"].plot(title = 'BTCEUR', legend = 'open')
data_df["close"].plot(title = 'BTCEUR', legend = 'close')
data_df["volume"].plot(title = 'BTCEUR', legend = 'volume')
plt.show()


# ### test des time series périodiques
# 
# 
# # stats_model, fbprophet ou ARIMA

# 
# ### statsmodels
# 
# 
# 

import pandas as pd 
import numpy as np 
from statsmodels.tsa.seasonal import seasonal_decompose

# help(seasonal_decompose)


result = seasonal_decompose(data_df["close"], model='additive', period=1)


#result["open"].plot(title = 'BTCEUR', legend = 'open')
#result["close"].plot(title = 'BTCEUR', legend = 'close')
#result["volume"].plot(title = 'BTCEUR', legend = 'volume')
#plt.show()
result.plot()
plt.show()

result.trend


result.seasonal


result.resid

