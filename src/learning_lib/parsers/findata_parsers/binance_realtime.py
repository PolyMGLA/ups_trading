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
from colorama import init
init()
from colorama import Fore, Back, Style
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

TIMEZONE = datetime.fromtimestamp(0) - datetime.utcfromtimestamp(0)
COLUMNS = ['openTime', 'open', 'high', 'low', 'close', 'baseVolume', 'closeTime', 'quoteVolume', 'numTrades',
                 'takerBuyBaseVolume', 'takerBuyQuoteVolume', 'unused']

def request_candles(API_PATH: str,
                    csv_save_pth: str,
                    symbol: str,
                    interval: str,
                    startTime: str,
                    endTime: str,
                    EXPORT: bool = False) -> pd.DataFrame:
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

    candles = pd.DataFrame(
        result,
        columns=COLUMNS
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

    if EXPORT: candles.to_csv(csv_save_pth, index=False)
    time.sleep(1)
    return candles

class BinanceRealtimeParser(Thread):
    """
    Процесс парсинга данных с Binance в реальном времени
    Перед запуском через .start() необходимо вызвать .init()
    """
    running = True
    tick = []
    parsed = { }
    dir = ""
    EXPORT = True

    def init(self,
             tick: list[str],
             EXPORT: bool = False,
             dir: str = "src/data") -> None:
        """
        Инициализирует список токенов и флаг экспорта
        :param tick: Отслеживаемые тикеры
        :param EXPORT: True, чтобы автоматически сохранять данные после каждой итерации
        :param dir: папка для экспорта
        """
        self.tick = tick
        self.parsed = { ticker : pd.DataFrame(columns=['openTime', 'closeTime', 'open', 'high', 'low', 'close', 'baseVolume',
            'quoteVolume', 'numTrades', 'takerBuyBaseVolume',
            'takerBuyQuoteVolume']) for ticker in tick }
        self.EXPORT = EXPORT
        self.dir = dir

    def run(self):
        print(Fore.YELLOW + "started binance realtime parser", Style.RESET_ALL)
        if not os.path.exists(self.dir):
            print(Fore.RED + f"{self.dir} not found, creating..", Style.RESET_ALL)
            os.mkdir(self.dir)

        next = datetime.now()
        while self.running:
            dt = datetime.now().replace(microsecond=0)
            if dt >= next:
                next = dt + timedelta(minutes=5)
            else:
                time.sleep(1)
                continue
            print(Style.BRIGHT + "parsing candle:", dt, "-", next, Style.RESET_ALL)
            t = tqdm(self.tick, file=sys.stdout)
            for tick_symbol in self.tick:
                df = request_candles(
                    FUT_API_PATH,
                    f"{self.dir}/{tick_symbol}.csv",
                    [tick_symbol],
                    '5m',
                    (dt - timedelta(minutes=6) - TIMEZONE).isoformat(),
                    (dt - timedelta(minutes=1) - TIMEZONE).isoformat(),
                    EXPORT=False
                )
                self.parsed[tick_symbol] = pd.concat([self.parsed[tick_symbol], df])
                t.update(1)
                t.refresh()
            t.close()
            if self.EXPORT:
                self._export()

    def fetch(self) -> dict[str, pd.DataFrame]:
        """
        Возвращает распаршенные данные и очищает их локально
        """
        p = self.parsed.copy()
        self.parsed = { }
        return p

    def stop(self) -> None:
        """
        Просто останавливает выполнение потока
        """
        self.running = False
    
    def _import(self,
                tickers: list[str] = None) -> None:
        """
        Импортирует данные по указанным тикерам из /src/data/*.csv
        :param tickers: список требуемых тикеров. Если None, импортируются все
        """
        if tickers is None:
            tickers = self.tick

        if not os.path.exists(self.dir):
            print(Fore.RED + f"{self.dir} not found, creating..", Style.RESET_ALL)
            os.mkdir(self.dir)

        print(f"importing data from {self.dir}", end=" ")
        try:
            for el in tickers:
                if not os.path.exists(f"{self.dir}/{el}.csv"):
                    print(Fore.RED + f"{self.dir}/{el}.csv not found", Style.RESET_ALL)
                    continue
                self.parsed[el] = pd.read_csv(f"{self.dir}/{el}.csv")
        except Exception as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "done" + Style.RESET_ALL)

    def _export(self,
                tickers: list[str] = None) -> None:
        """
        Сохранить данные по указанным тикерам в /src/data/*.csv
        :param tickers: список требуемых тикеров. Если None, сохранятся все
        """
        if tickers is None:
            tickers = self.tick

        if not os.path.exists(self.dir):
            print(Fore.RED + f"{self.dir} not found, creating..", Style.RESET_ALL)
            os.mkdir(self.dir)
        
        for el in tickers:
            self.parsed[el].to_csv(f"{self.dir}/{el}.csv", index=False)

if __name__ == "__main__":
    with open("src/learning_lib/parsers/findata_parsers/tokens_names.txt") as f:
        tick = [line.strip() for line in f.readlines()]
    parser = BinanceRealtimeParser()
    parser.init(tick, EXPORT=True)
    #True, чтобы автоматически сохранять данные после каждой итерации
    parser.start()