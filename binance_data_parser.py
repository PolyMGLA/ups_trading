import os
import pandas as pd
import requests

from tqdm.notebook import tqdm
from joblib import delayed, Parallel
from binance.client import Client, HistoricalKlinesType

API = os.getenv('key')
SECRET = os.getenv('secret')

client = Client(API, SECRET)

def dataloader(ticker, interval, start_time=None, stop_time=None, klines_type=HistoricalKlinesType.FUTURES):
    data = pd.DataFrame(
    client.get_historical_klines(ticker, interval, start_str=start_time, end_str=stop_time, klines_type=klines_type),
    columns=['open_time','open', 'high', 'low', 'close', 'volume','close_time', 'qav','num_trades','taker_base_vol','taker_quote_vol', 'ignore']
    )
    data.index = pd.to_datetime(data['open_time'] * 1_000_000)
    data.drop(columns=['open_time', 'close_time', 'ignore'], inplace=True)
    data['open'] = data['open'].astype('float')
    data['close'] = data['close'].astype('float')
    data['high'] = data['high'].astype('float')
    data['low'] = data['low'].astype('float')
    data['volume'] = data['volume'].astype('float')
    data['qav'] = data['qav'].astype('float')
    data['taker_base_vol'] = data['taker_base_vol'].astype('float')
    data['taker_quote_vol'] = data['taker_quote_vol'].astype('float')
    return data

BINANCE_ROOT_PATH = 'https://www.binance.com'

SPOT_API_PATH = BINANCE_ROOT_PATH + '/api/v3'
FUT_API_PATH = BINANCE_ROOT_PATH + '/fapi/v1'


def get_symbols(API_PATH):
    R = requests.get(url=API_PATH + '/exchangeInfo')
    result = R.json()
    return pd.DataFrame([
        {key: item[key] for key in ['symbol', 'status', 'baseAsset', 'quoteAsset']}
        for item in result['symbols']
    ])

TICKERS = get_symbols(FUT_API_PATH)['symbol'].to_list()

def process_tick_joblib(ticker):
    data = dataloader(
        ticker,
        '5m',
        '01.01.2022',
        '12.12.2025'
    )
    data.to_csv(f'{ticker}.csv')

Parallel(n_jobs=-1)(delayed(process_tick_joblib)(ticker) for ticker in tqdm(TICKERS[:50]))