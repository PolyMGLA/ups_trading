import os, sys
import datetime
from learning_lib.parsers.findata_parsers.binance_realtime import BinanceRealtimeParser
from learning_lib.parsers.news_parsers.coindesk_realtime import CoinDeskRealTimeParser
from learning_lib.models.lstm import LSTMModel
from learning_lib.models.nlp import NLPModel
from learning_lib.models.merge_predictions import PredictionMerger
from server import Server

import time

#TODO: 
# Инициализация парсеров
# Инициализация моделей
# Поддержка сервера

binance_parser = BinanceRealtimeParser()
coin_parser = CoinDeskRealTimeParser()
lstm_model = LSTMModel()
nlp_model = NLPModel()
merger = PredictionMerger()
server = Server()

if __name__ == "__main__":
    with open("src/learning_lib/parsers/findata_parsers/tokens_names.txt") as f:
        tick = [line.strip() for line in f.readlines()]
    binance_parser.init(tick, EXPORT=True)
    coin_parser.init(EXPORT=True)

    server.start()
    coin_parser.start()

    time.sleep(3)
    binance_parser.start()