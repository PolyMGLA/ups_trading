import datetime
from dateutil.parser import parse as parse_date
import itertools
import time
import os
import sys
import numpy as np
import pandas as pd
import requests
import json
import pytz
from tqdm import tqdm
import pathlib
from threading import Thread

from datetime import timedelta,datetime
from dateutil.parser import parse as parse_date
from pytz import utc
from time import sleep
from joblib import delayed, Parallel
import nest_asyncio
nest_asyncio.apply()

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

BINANCE_ROOT_PATH = 'https://www.binance.com'

SPOT_API_PATH = BINANCE_ROOT_PATH + '/api/v3'
FUT_API_PATH = BINANCE_ROOT_PATH + '/fapi/v1'

TIMEZONE = 3


def get_symbols(API_PATH):
    R = requests.get(url=API_PATH + '/exchangeInfo')
    result = R.json()
    return pd.DataFrame([
        {key: item[key] for key in ['symbol', 'status', 'baseAsset', 'quoteAsset']}
        for item in result['symbols']
    ])


tickers = get_symbols(FUT_API_PATH)
tick = tickers['symbol'].to_list()


def request_candles(API_PATH, csv_save_pth, symbol, interval, startTime, endTime, with_loop=True):
    '''
    API_PATH - откуда будем парсить
    symbol - наименование валюты
    interval : 1s,1m,3m,5m,15m,30m,1h,2h,3h,4h,6h,8h,12h,1d,1w,1M - интервал времени, ширина одной свечи
    startTime, endTime required to be in UTC - старт и конец времени сбора данных
    '''

    dt = parse_date(startTime)
    dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzinfo=utc)
    startTime = int(1000 * dt.timestamp())

    dt = parse_date(endTime)
    dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzinfo=utc)
    endTime = int(1000 * dt.timestamp())

    result = list()
    if with_loop:
        while startTime < endTime:
            # print ('Now requesting : {} --- {}'.format(datetime.fromtimestamp(1e-3*startTime,tz=utc).strftime('%Y-%m-%d %H:%M:%S'),datetime.fromtimestamp(1e-3*endTime,tz=utc).strftime('%Y-%m-%d %H:%M:%S')))
            while True:
                R = requests.get(
                    API_PATH + '/klines',
                    params={
                        'symbol': symbol,
                        'interval': interval,
                        'limit': 1000,
                        'startTime': startTime,
                        'endTime': endTime - 1,
                    }
                )
                if R.ok:
                    break
                else:
                    print(R.text)
                    sleep(30)
            iteration_result = R.json()
            if not len(iteration_result):
                break
            result += iteration_result
            startTime = iteration_result[-1][6] + 1
    else:
        R = requests.get(
            API_PATH + '/klines',
            params={
                'symbol': symbol,
                'interval': interval,
                'limit': 10,
                'startTime': startTime,
                'endTime': endTime,
            }
        )
        result = R.json()

    candles = pd.DataFrame(
        result,
        columns=['openTime', 'open', 'high', 'low', 'close', 'baseVolume', 'closeTime', 'quoteVolume', 'numTrades',
                 'takerBuyBaseVolume', 'takerBuyQuoteVolume', 'unused']
    ).astype({
        'open': float,
        'high': float,
        'low': float,
        'close': float,
        'baseVolume': float,
        'quoteVolume': float,
        'takerBuyBaseVolume': float,
        'takerBuyQuoteVolume': float
    })[
        ['openTime', 'closeTime', 'open', 'high', 'low', 'close', 'baseVolume', 'quoteVolume', 'numTrades',
         'takerBuyBaseVolume', 'takerBuyQuoteVolume']
    ]

    for f in ['openTime', 'closeTime']:
        candles[f] = candles[f].apply(lambda x: datetime.fromtimestamp(1e-3 * x, tz=utc))

    candles.to_csv(csv_save_pth, index=False)
    time.sleep(1)
    return candles


def binance_parse_candles_all_symbols(transaction_types_apis, symbols_names, start_time, end_time, save_dir, interval):
    start_time_timestamp = parse_date(start_time)
    end_time_timestamp = parse_date(end_time)

    if os.path.exists(save_dir):
        print(f"Папка {save_dir} найдена, начинаю парсинг...")
    else:
        pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
        print(f"Папка {save_dir} не найдена и была создана, начинаю парсинг...")

    for i in itertools.product(transaction_types_apis, symbols_names,
                               range(start_time_timestamp.year, end_time_timestamp.year + 1)):
        API_path, symb, int_year = i
        type = str(API_path).replace('/', '_').replace('.', '_').replace(':', '_')
        year = str(int_year)
        candle_save_pth = save_dir + '/' + type + '/' + symb + '/'
        pathlib.Path(candle_save_pth).mkdir(parents=True, exist_ok=True)

        start_timestamp_req = datetime(year=int_year, month=1, day=1)
        end_timestamp_req = datetime(year=int_year + 1, month=1, day=1) - timedelta(days=1)
        if int_year == start_time_timestamp.year:
            start_timestamp_req = start_time_timestamp
        if int_year == end_time_timestamp.year:
            end_timestamp_req = end_time_timestamp

        print(f"Сейчас собираю {candle_save_pth}{year}.csv...")
        request_candles(API_path,
                        candle_save_pth + f"{year}.csv",
                        symb,
                        interval,
                        datetime.strftime(start_timestamp_req, format='%d/%m/%Y, %H:%M:%S'),
                        datetime.strftime(end_timestamp_req, format='%d/%m/%Y, %H:%M:%S'))
        print(f"Собрал {candle_save_pth}{year}.csv!")

        # Операции с датафреймом
        print(f"Проверка {candle_save_pth}{year}.csv на выборсы и пропуски...")
        csv_dat = pd.read_csv(candle_save_pth + f"{year}.csv")
        csv_dat = csv_dat.dropna(axis=0)
        print(f"Найдено пропусков: {csv_dat.isna().sum(axis=1).sum()}")
        csv_dat.to_csv(candle_save_pth + f"{year}.csv")
        print(f"Успешно сохранён {candle_save_pth}{year}.csv")
        print('\n')

tick = []

class BinanceRealtimeParser(Thread):
    """
    Процесс парсинга данных с Binance в реальном времени
    Перед запуском через .start() необходимо вызвать .init()
    """
    running = True
    tick = []
    parsed = { }
    EXPORT = True

    def init(self, tick, EXPORT=False):
        """
        Инициализирует список токенов и флаг экспорта
        :param tick: Отслеживаемые тикеры
        :param EXPORT: True, чтобы автоматически сохранять данные после каждой итерации
        """
        self.tick = tick
        self.parsed = { ticker : pd.DataFrame(columns=['openTime', 'closeTime', 'open', 'high', 'low', 'close', 'baseVolume',
            'quoteVolume', 'numTrades', 'takerBuyBaseVolume',
            'takerBuyQuoteVolume']) for ticker in tick }
        self.EXPORT = EXPORT

    def run(self):
        if not os.path.exists("src/data"):
            os.mkdir("src/data")

        next = datetime.now()
        while self.running:
            dt = datetime.now()
            if dt >= next:
                next = dt + timedelta(minutes=5)
            else:
                time.sleep(1)
                continue
            print(dt, next)
            for tick_symbol in tqdm(self.tick):
                df = request_candles(
                    FUT_API_PATH,
                    f"src/data/{tick_symbol}.csv",
                    [tick_symbol],
                    '5m',
                    (dt - timedelta(minutes=6, hours=TIMEZONE)).isoformat(),
                    (dt - timedelta(minutes=1, hours=TIMEZONE)).isoformat(),
                )
                self.parsed[tick_symbol] = pd.concat([self.parsed[tick_symbol], df])
            if self.EXPORT:
                self._export()

    def fetch(self):
        """
        Возвращает распаршенные данные и очищает их локально
        """
        p = self.parsed.copy()
        self.parsed = { }
        return p

    def stop(self):
        """
        Просто останавливает выполнение потока
        """
        self.running = False
    
    def _import(self, tickers=None):
        """
        Импортирует данные по указанным тикерам из /src/data/*.csv
        :param tickers: список требуемых тикеров. Если None, импортируются все
        """
        if tickers is None:
            tickers = self.tick

        if not os.path.exists("src/data"):
            os.mkdir("src/data")
        
        for el in tickers:
            if not os.path.exists(f"src/data/{el}.csv"):
                print(f"src/data/{el}.csv not found")
                continue
            self.parsed[el] = pd.read_csv(f"src/data/{el}.csv")

    def _export(self, tickers=None):
        """
        Сохранить данные по указанным тикерам в /src/data/*.csv
        :param tickers: список требуемых тикеров. Если None, сохранятся все
        """
        if tickers is None:
            tickers = self.tick

        if not os.path.exists("src/data"):
            os.mkdir("src/data")
        
        for el in tickers:
            self.parsed[el].to_csv(f"src/data/{el}.csv", index=False)

if __name__ == "__main__":
    with open("src/learning_lib/parsers/findata_parsers/tokens_names.txt") as f:
        tick = [line.strip() for line in f.readlines()]
    parser = BinanceRealtimeParser()
    parser.init(tick, EXPORT=False)
    #True, чтобы автоматически сохранять данные после каждой итерации
    parser.start()