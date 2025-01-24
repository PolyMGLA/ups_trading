import os, sys
import datetime
from learning_lib.parsers.findata_parsers.binance_realtime import BinanceRealtimeParser
from learning_lib.parsers.news_parsers.coindesk_realtime import CoinDeskRealTimeParser

#TODO: 
# Инициализация парсеров
# Инициализация моделей
# Поддержка сервера

if __name__ == "__main__":
    # os.system("cd ../front/src/frontend && pnpm dev")
    with open("src/learning_lib/parsers/findata_parsers/tokens_names.txt") as f:
        tick = [line.strip() for line in f.readlines()]
    binance_parser = BinanceRealtimeParser()
    binance_parser.init(tick, EXPORT=True)
    coin_parser = CoinDeskRealTimeParser()
    coin_parser.init(EXPORT=True)
    binance_parser.start()
    coin_parser.start()