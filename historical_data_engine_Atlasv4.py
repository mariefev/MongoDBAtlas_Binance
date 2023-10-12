# Engine to extract all trading pairs crypto market data
# Terminal command : python3 -u historical_data_engine_Atlasv4.py > results/load_engine_Atlasv4.txt
# -u allows to follow the process live within engine_Atlasv4.txt

import requests
import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    t0 = time.time()
    print("START - {}\n".format(dt.datetime.fromtimestamp(t0).strftime("%Y-%m-%d %H:%M:%S"),3))

    # Data source used: Binance API url
    url = 'https://api.binance.com/api/v3/klines'

    # Market to study
    money = 'BTC'

    # Interval between records
    # 1M = 1 month, 1h = 1 hour, 1m = 1 minute, 1s = 1 second
    #interval = '1m'
    interval = '1d'

    # Period extracted
    # start_period = dt.datetime(2020, 1, 1)
    start_period = dt.datetime(2021, 1, 1)
    # end_period = dt.datetime(2023, 8, 26)
    # end_period = dt.datetime(2020, 1, 2)
    end_period = dt.datetime(2023, 9, 1)

    # Trading pairs list (ex: all pairs for ETH)
    trading_pairs = get_trading_pairs(money)

    # Connect Mongo
    client, markets = connect_mongo_atlas()

    # Loop to get data for each trading pair
    for pair in trading_pairs:
        print('Market: ',pair)
        engine(url, pair, interval, start_period, end_period, markets)

    # Close Mongo
    client.close()

    tt = (time.time() - t0) / 60
    print("\nRealized in {} minutes".format(round(tt,3)))
    print("\nEND - {}\n".format(dt.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")))


def connect_mongo_atlas():
    load_dotenv()
    user=os.getenv("ATLAS_USER")
    pwd=os.getenv("ATLAS_PWD")
    print(user, pwd)
    clustername="Cluster1"
    uri = "mongodb+srv://{0}:{1}@{2}.sgf90rd.mongodb.net/?retryWrites=true&w=majority".format(user, pwd, clustername)
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!", uri)
    except Exception as e:
        print(e)

    # Database creation
    binance_historical = client['binance_historical_All_BTC']
    print("connexion à MongoDB Atlas avec ", os.getenv('ATLAS_USER'),os.getenv('ATLAS_PWD'))
    # Collection creation
    markets = binance_historical.create_collection(name="BTC_markets")
    return client, markets


def get_trading_pairs(money):
    market_list = get_market_list()
    money_trading_pairs = get_pairs(money, market_list)
    return money_trading_pairs

def get_market_list():
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    data = response.json()

    trading_pairs = []
    for symbol_info in data['symbols']:
        trading_pairs.append(symbol_info['symbol'])

    return trading_pairs

def get_pairs(money, market_list):
    df = pd.DataFrame(market_list)
    df.columns = ['pairs']
    df = df[df.pairs.str.startswith(money)]
    df = df.reset_index()
    return df.pairs

# data request, data cleaning, data integration in MongoDB
def engine(url, symbol, interval, start_period, end_period, markets):

    # Size of each period of time request to respect API restriction
    day_period = get_chunk(start_period, end_period, interval)

    data = get_data(url, symbol, interval, start_period, end_period, day_period)

    if data:
        df_data = create_df(data, symbol)
        df_clean = clean_df(df_data)

        # Display or use data_df as needed
        # print("\n",df_clean.close.describe())
        # print('df_clean.close count: ', df_clean.close.count())

        # Chart
        # df_clean["close"].plot(title = 'ETHEUR', legend = 'close')
        # plt.show()

        # MongoDB market data upload
        mongo_upload(df_clean, markets)


# API limitation - 500 records per call
# Number of calls that will be necessary to extract data
def get_chunk(start_period, end_period, interval):
    time_difference = end_period - start_period
    # Evaluation of the max number of records that could be extracted
    if interval == '1m':
        nbr_records = time_difference.total_seconds() / 60
    else:
        nbr_records = time_difference.total_seconds() / 3600
    # Number of necessary calls to get all records
    nbr_calls = nbr_records/500
    # size period calculation (nbr of days to get 500 records)
    return pd.Timedelta(days=time_difference.days / nbr_calls)

def get_data(url, symbol, interval, start_period, end_period, day_period):
    data = []
    request_limit_per_second = 20
    # Used to organize minimal sleep to respect API limitation nbr requests
    time_interval = pd.Timedelta(seconds=1 / request_limit_per_second).total_seconds()
    cycle = 1

    while start_period < end_period:
        # Calculate the remaining time between start_period and end_period
        remaining_time = end_period - start_period

        # Adjust the day_period for the last chunk based on the remaining time
        if remaining_time < day_period:
            day_period = remaining_time

        # Sleep to respect API rate limit
        if cycle % 20 == 0:
            time.sleep(time_interval)
            # interval 1h
            # print('cycle: ',cycle)
        # interval 1m
        if cycle == 1 or cycle == 10 or cycle % 800 == 0:
            print('cycle: ',cycle)

        start_period_str = str(int(start_period.timestamp() * 1000))
        end_period_str = str(int((start_period + day_period).timestamp() * 1000))

        par = {'symbol': symbol, 'interval': interval, 'startTime': start_period_str, 'endTime': end_period_str}

        try:
            response = requests.get(url, params=par)
            response.raise_for_status()  # Raise an exception if response status code is not 2xx
            data.extend(json.loads(response.text))
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")

        # Move to the next time interval
        start_period += day_period + pd.Timedelta(days=1)
        cycle += 1

    return data

def create_df(data, symbol):
    # Create DataFrame
    df_data = pd.DataFrame(data)
    df_data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'nbr_trades','taker_base_vol', 'taker_quote_vol', 'unused_field']
    df_data.index = [dt.datetime.fromtimestamp(d/1000.0) for d in df_data.datetime]
    df_data = df_data.sort_index()
    df_data = df_data.astype(float)
    df_data['market'] = symbol
    df_data['date'] = [dt.datetime.fromtimestamp(d/1000.0) for d in df_data.datetime]
    return df_data

def clean_df(df_data):
    # Check if data is clean
    # df_data.isna().sum()
    # Remove NaN
    df_data = df_data.dropna(axis = 1,how='any')
    # Remove 0
    df_data = df_data[df_data.close != 0]
    return df_data

def mongo_upload(df_clean, markets):
    # Convert DataFrame to list of dictionaries
    formatted_data = df_clean.to_dict('records')

    # Insert data into MongoDB
    markets.insert_many(formatted_data)

# To automatically launch main from terminal
if __name__ == "__main__":
    main()