import numpy as np
import pandas as pd
import os
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

#load_dotenv()

API_KEY = os.getenv('API')
API_SECRET = os.getenv('SECRET')

client = Client(API_KEY, API_SECRET)

def binanceDataFrame(klines):
    df = pd.DataFrame(
        klines.reshape(-1,12),
        dtype=float,
        columns = (
            'Open Time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close time',
            'Quote asset volume',
            'Number of trades',
            'Taker buy base asset volume',
            'Taker buy quote asset volume',
            'Ignore'
        )
    )
    df['Open Time'] = pd.to_datetime(
        df['Open Time'],
        unit='ms'
    )
    df.rename(
        columns={
            'Open Time': 'time',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        },
        inplace=True
    )
    df.index = df['time']
    df.drop(
        columns=[
            'time',
            'Quote asset volume',
            'Number of trades',
            'Taker buy base asset volume',
            'Taker buy quote asset volume',
            'Ignore',
            'Close time'
        ],
        inplace=True
    )

    return df

def parse_tickers(TICKERS, CANDLETIME, STARTDATE):

    close = {}
    open = {}
    high = {}
    low = {}
    volume = {}

    for ticker in TICKERS:
        data = binanceDataFrame(
            np.array(
                client.get_historical_klines(
                    ticker,
                    CANDLETIME,
                    STARTDATE
                )
            )
        )
        close[ticker] = data['close']
        open[ticker] = data['open']
        high[ticker] = data['high']
        low[ticker] = data['low']
        volume[ticker] = data['volume']
    
    close = pd.concat(close, axis=1)
    open = pd.concat(open, axis=1)
    high = pd.concat(high, axis=1)
    low = pd.concat(low, axis=1)
    volume = pd.concat(volume, axis=1)

    returns = close.pct_change().shift(-1).dropna()
    return close, open, high, low, volume, returns

def neutralize(alpha):
    return alpha - alpha.mean(axis=1)

def scale(alpha):
    return alpha.div(
        alpha
        .abs()
        .sum(axis=1),
        axis=0
    )