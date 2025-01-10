import datetime
from dateutil.parser import parse as parse_date
import itertools

import os
import sys
import numpy as np
import pandas as pd
import requests
import json
import pytz
import pathlib

from datetime import timedelta,datetime
from dateutil.parser import parse as parse_date
from pytz import utc
from time import sleep
from tqdm.notebook import tqdm

import nest_asyncio
nest_asyncio.apply()

def request_candles(API_PATH, csv_save_pth, symbol, interval, startTime, endTime, with_loop=True):
    '''
    API_PATH - откуда будем парсить
    symbol - наименование валюты
    interval : 1s,1m,3m,5m,15m,30m,1h,2h,3h,4h,6h,8h,12h,1d,1w,1M - интервал времени, ширина одной свечи
    startTime, endTime required to be in UTC - старт и конец времени сбора данных
    '''
    
    dt = parse_date(startTime)
    dt = datetime(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,dt.microsecond,tzinfo=utc)
    startTime = int(1000*dt.timestamp())

    dt = parse_date(endTime)
    dt = datetime(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,dt.microsecond,tzinfo=utc)
    endTime = int(1000*dt.timestamp())
    
    result = list()
    if with_loop:
        while startTime < endTime:
            # print ('Now requesting : {} --- {}'.format(datetime.fromtimestamp(1e-3*startTime,tz=utc).strftime('%Y-%m-%d %H:%M:%S'),datetime.fromtimestamp(1e-3*endTime,tz=utc).strftime('%Y-%m-%d %H:%M:%S')))
            while True:
                R = requests.get(
                    API_PATH + '/klines',
                    params = {
                        'symbol' : symbol,
                        'interval' : interval,
                        'limit' : 1000,
                        'startTime' : startTime,
                        'endTime' : endTime-1,
                    }
                )
                if R.ok:
                    break
                else:
                    print (R.text)
                    sleep(30)
            iteration_result = R.json()
            if not len(iteration_result):
                break
            result += iteration_result
            startTime = iteration_result[-1][6]+1
    else:
        R = requests.get(
                    API_PATH + '/klines',
                    params = {
                        'symbol' : symbol,
                        'interval' : interval,
                        'limit' : 10,
                        'startTime' : startTime,
                        'endTime' : endTime,
                    }
                )
        result = R.json()
    
    candles = pd.DataFrame(
        result,
         columns = ['openTime', 'open', 'high', 'low', 'close', 'baseVolume', 'closeTime', 'quoteVolume', 'numTrades', 'takerBuyBaseVolume', 'takerBuyQuoteVolume', 'unused']
    ).astype({
        'open' : float,
        'high' : float,
        'low' : float,
        'close' : float,
        'baseVolume' : float,
        'quoteVolume' : float,
        'takerBuyBaseVolume' : float,
        'takerBuyQuoteVolume' : float
    })[
        ['openTime', 'closeTime', 'open', 'high', 'low', 'close', 'baseVolume', 'quoteVolume', 'numTrades', 'takerBuyBaseVolume', 'takerBuyQuoteVolume']
    ]

    for f in ['openTime','closeTime']:
        candles[f] = candles[f].apply(lambda x : datetime.fromtimestamp(1e-3*x,tz=utc))
    
    candles.to_csv(csv_save_pth)
    return candles

def binance_parse_candles_all_symbols(transaction_types_apis, symbols_names, start_time, end_time, save_dir, interval):
    start_time_timestamp = parse_date(start_time)
    end_time_timestamp = parse_date(end_time)

    if os.path.exists(save_dir):
            print(f"Папка {save_dir} найдена, начинаю парсинг...")
    else:
        pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
        print(f"Папка {save_dir} не найдена и была создана, начинаю парсинг...")

    for i in itertools.product(transaction_types_apis, symbols_names, range(start_time_timestamp.year, end_time_timestamp.year+1)):
        API_path, symb, int_year = i
        type = str(API_path).replace('/', '_').replace('.', '_').replace(':', '_')
        year = str(int_year)
        candle_save_pth = save_dir + '/' + type + '/' + symb + '/'
        pathlib.Path(candle_save_pth).mkdir(parents=True, exist_ok=True)

        start_timestamp_req = datetime(year = int_year, month=1, day = 1)
        end_timestamp_req = datetime(year = int_year+1, month=1, day = 1) - timedelta(days=1)
        if int_year == start_time_timestamp.year:
            start_timestamp_req = start_time_timestamp
        if int_year == end_time_timestamp.year:
            end_timestamp_req = end_time_timestamp

        print(f"Сейчас собираю {candle_save_pth}{year}.csv...")
        request_candles(API_path,
                        candle_save_pth+f"{year}.csv", 
                        symb, 
                        '5m', 
                        datetime.strftime(start_timestamp_req, format='%d/%m/%Y, %H:%M:%S'), 
                        datetime.strftime(end_timestamp_req, format='%d/%m/%Y, %H:%M:%S'))
        print(f"Собрал {candle_save_pth}{year}.csv!")

        #Операции с датафреймом
        print(f"Проверка {candle_save_pth}{year}.csv на выборсы и пропуски...")
        csv_dat = pd.read_csv(candle_save_pth+f"{year}.csv")
        csv_dat = csv_dat.dropna(axis=0)
        print(f"Найдено пропусков: {csv_dat.isna().sum(axis=1).sum()}")
        csv_dat.to_csv(candle_save_pth+f"{year}.csv")
        print(f"Успешно сохранён {candle_save_pth}{year}.csv")
        print('\n')

BINANCE_ROOT_PATH = 'https://www.binance.com'
SPOT_API_PATH = BINANCE_ROOT_PATH + '/api/v3'
FUT_API_PATH = BINANCE_ROOT_PATH + '/fapi/v1'

if __name__ == "__main__":
    binance_parse_candles_all_symbols(
        [SPOT_API_PATH, FUT_API_PATH],
        ['BTCUSDT'],
        '1.2.2024',
        '1.3.2024',
        'Vallet_Courses_Loader/data',
        '5m')