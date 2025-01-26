import os, sys
import datetime
import time
from colorama import init
init()
from colorama import Fore, Back, Style

from learning_lib.parsers.findata_parsers.binance_realtime import BinanceRealtimeParser, concat
from learning_lib.parsers.news_parsers.coindesk_realtime import CoinDeskRealTimeParser
from learning_lib.models.lstm import LSTMModel
from learning_lib.models.nlp import NLPModel
from learning_lib.models.merge_predictions import PredictionMerger
from learning_lib.utils.strategy_update import StrategyUpdater
from server import Server
import numpy as np
import torch as pt
import pandas as pd

IMPORT_FINDATA = False
IMPORT_NEWSDATA = True

#TODO: 
# Инициализация парсеров done
# Инициализация моделей done
# Поддержка сервера done
# Поток передачи данных с моделей на сервер

binance_parser = BinanceRealtimeParser()
coin_parser = CoinDeskRealTimeParser()
lstm_model = LSTMModel()
nlp_model = NLPModel()
merger = PredictionMerger()
updater = StrategyUpdater()
server = Server()

cols = ["open", "high", "low", "close", "baseVolume", "quoteVolume",
        "numTrades", "takerBuyBaseVolume", "takerBuyQuoteVolume"]

if __name__ == "__main__":
    with open("src/learning_lib/parsers/findata_parsers/tokens_names.txt") as f:
        tick = [line.strip() for line in f.readlines()]
    binance_parser.init(tick, EXPORT=True)
    coin_parser.init(EXPORT=True)

    if IMPORT_NEWSDATA:
        coin_parser._import("coindesk_news.json")
    else:
        print("importing data from coindesk_news.json" + Fore.YELLOW, "skip", Style.RESET_ALL)

    if IMPORT_FINDATA:
        binance_parser._import(None)
    else:
        print(f"importing data from src/data" + Fore.YELLOW, "skip", Style.RESET_ALL)
    
    server.start()

    num = 10

    try:
        findata = concat(binance_parser.request(None), tick)
    except Exception as e:
        print(f"parsing last {num} candles..", Fore.RED + "error")
        print(str(e) + Style.RESET_ALL)
    else:
        print(f"parsing last {num} candles..", Fore.GREEN + "done" + Style.RESET_ALL)

    coin_parser.start()
    binance_parser.start()

    time.sleep(1)

    while True:
        if not binance_parser.done:
            time.sleep(1)
            continue
        d = concat(binance_parser.fetch(), tick)
        findata = pd.concat([findata, d])
        findata = findata.iloc[1:]
        print(findata)
        # pred = lstm_model.predict(findata)
        # print(pred)
        # ждем следующей свечи
