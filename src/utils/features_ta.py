import pandas as pd
import numpy as np
import pandas_ta as ta

def check_features(df: pd.Series,
                    length_sma: int,
                    length_ema: int,
                    length_mom: int,
                    length_rsi: int,
                    adx_length: int,
                    drift_pvt: int,
                    atr_length: int,
                    bbands_length) -> bool:
    if df[f'RSI_{length_rsi}'] <= 20 and df[f'ATRr_{atr_length}'].mean() * 0.9 <= df[f'ATRr_{atr_length}'] <= df[f'ATRr_{atr_length}'].mean() * 1.1:
        return True
    if df[f'RSI_{length_rsi}'] >= 80 and df[f'ATRr_{atr_length}'].mean() * 0.9 <= df[f'ATRr_{atr_length}'] <= df[f'ATRr_{atr_length}'].mean() * 1.1:
        return False
    if df[f'MACDh_{12}_{26}_{9}'] > 0 and df[f'RSI_{length_rsi}'] <= 20:
        return True
    if df[f'MACDh_{12}_{26}_{9}'] < 0 and df[f'RSI_{length_rsi}'] >= 80:
        return False
    if df['close'] > df[f'EMA_{length_ema}'] and df[f'RSI_{length_rsi}'] <= 20:
        return True
    if df['close'] < df[f'EMA_{length_ema}'] and df[f'RSI_{length_rsi}'] >= 80:
        return False
    if df[f'RSI_{length_rsi}'] <= 20 and df[f'STOCH'] <= 20:
        return True
    if df[f'RSI_{length_rsi}'] >= 80 and df[f'STOCH'] >= 80:
        return False
    if df[f'MACD_{12}_{26}_{9}'] > 0 and df['close'] > df[f'EMA_{length_ema}']:
        return True
    if df[f'MACD_{12}_{26}_{9}'] < 0 and df['close'] < df[f'EMA_{length_ema}']:
        return False
    if df[f'EMA_50'] > df[f'EMA_200'] and df[f'EMA_50'].shift(1) <= df[f'EMA_200'].shift(1):
        return True
    if df[f'EMA_50'] < df[f'EMA_200'] and df[f'EMA_50'].shift(1) >= df[f'EMA_200'].shift(1):
        return False
    if df[f'RSI_{length_rsi}'] > df[f'RSI_{length_rsi}'].shift(1) and df['close'] < df['close'].shift(1):
        return True
    if df[f'RSI_{length_rsi}'] < df[f'RSI_{length_rsi}'].shift(1) and df['close'] > df['close'].shift(1):
        return False
    if df['close'] <= df['BBL_20_2.0'] and df[f'ATRr_{atr_length}'].mean() * 0.9 <= df[f'ATRr_{atr_length}'] <= df[f'ATRr_{atr_length}'].mean() * 1.1:
        return True
    if df['close'] >= df['BBU_20_2.0'] and df[f'ATRr_{atr_length}'].mean() * 0.9 <= df[f'ATRr_{atr_length}'] <= df[f'ATRr_{atr_length}'].mean() * 1.1:
        return False
    if df['close'] <= df['BBL_20_2.0'] and df[f'MACD_{12}_{26}_{9}'] > 0:
        return True
    if df['close'] >= df['BBU_20_2.0'] and df[f'MACD_{12}_{26}_{9}'] < 0:
        return False
    if df['close'] <= df['BBL_20_2.0'] and df['close'] > df[f'EMA_{length_ema}']:
        return True
    if df['close'] >= df['BBU_20_2.0'] and df['close'] < df[f'EMA_{length_ema}']:
        return False
    if df[f'ADX_{adx_length}'] >= 25 and df[f'ATRr_{atr_length}'].mean() * 0.9 <= df[f'ATRr_{atr_length}'] <= df[f'ATRr_{atr_length}'].mean() * 1.1:
        return True
    if df[f'ADX_{adx_length}'] <= 20 and df[f'ATRr_{atr_length}'].mean() * 0.9 <= df[f'ATRr_{atr_length}'] <= df[f'ATRr_{atr_length}'].mean() * 1.1:
        return False
    if df['PVT'] > df['PVT'].shift(1) and df['close'] > df[f'EMA_{length_ema}']:
        return True
    if df['PVT'] < df['PVT'].shift(1) and df['close'] < df[f'EMA_{length_ema}']:
        return False


def get_features(df: pd.DataFrame,
                 length_sma: int,
                 length_ema: int,
                 length_mom: int,
                 length_rsi: int,
                 adx_length: int,
                 drift_pvt: int,
                 atr_length: int,
                 bbands_length):
    # SMA
    df.ta(kind='SMA', append=True, centered=False, close='close', length=length_sma)
    df['f_SMA'] = np.where(df['close'] > df[f'SMA_{length_sma}'], -1, 1)
    # EMA
    df.ta(kind='EMA', append=True, centered=False, close='close', length=length_ema)
    df['f_EMA'] = np.where(df['close'] > df[f'EMA_{length_ema}'], -1, 1)
    # ATR
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=atr_length)
    # YOUR MOM
    df.ta(kind='MOM', append=True, centered=False, close='close', length=length_mom)
    df['f_MOM'] = np.where(df[f'MOM_{length_mom}'] > 0, 1, -1)
    # RSI
    df.ta(kind='RSI', append=True, centered=False, close='close', length=length_rsi)
    df['f_RSI'] = np.where(df[f'RSI_{length_rsi}'] < 20, 1, np.where(df[f'RSI_{length_rsi}'] > 80, -1, 0))
    # ADX
    df.ta(kind='ADX', append=True, centered=False, close='close', length=adx_length)
    # ATR
    df.ta(kind='ATR', append=True, centered=False, high='high', low ='low', close='close', length=atr_length)
    atr_mean = df[f'ATRr_{atr_length}'].mean()
    situation_1 = (df[f'ADX_{adx_length}'] > 25) & (df[f'ATRr_{atr_length}'] > atr_mean)
    situation_2 = (df[f'ADX_{adx_length}'] < 20) & (df[f'ATRr_{atr_length}'] < atr_mean)
    df['f_ADX_ATR'] = np.where(situation_1, 1, np.where(situation_2, -1, 0))
    # PVT    
    df.ta(kind='PVT',append=True,centered=False,volume='volume',close='close', drift = drift_pvt)
    df['f_pvt'] = np.where(df['PVT'] > df['PVT'].rolling(window=12).mean(), 1, -1)

    df.ta(kind='MACD', close = 'close', fast = 12, slow = 26, signal = 9)
    df.ta(kind='STOCH', high = df['high'], low = df['low'], close = df['close'], k = 14, d = 3, smooth_k = 3)
    df.ta(kind='BBANDS', close = 'close', length = bbands_length, std = 2, ddof = 0)
    df['return_next_2'] = np.where(df['return_next'].shift(-2).rolling(window=3).sum() > 0, 1, -1)
    df['return_next_class'] = np.where(df['return_next'] > 0, 1, 0)
