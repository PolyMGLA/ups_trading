import os
import pandas as pd
from tqdm import tqdm
from typing import Dict


def tickers_transformer() -> None:
    """
    Функция для парсинга и преобразования данных о криптовалютах.
    
    Читает CSV файлы с историческими данными из директории 'data/raw_data',
    извлекает ключевые метрики (close, open, high, low и объемы) для каждого актива,
    объединяет их по тикерам и сохраняет в отдельные файлы в директорию 'data/clear_data'.

    Создаёт следующие файлы в директории 'clear_data':
    - close.csv
    - open.csv
    - high.csv
    - low.csv
    - baseVolume.csv
    - quoteVolume.csv
    - numTrades.csv
    - takerBuyBaseVolume.csv
    - takerBuyQuoteVolume.csv
    
    Все файлы содержат столбцы, соответствующие тикерам, и строки с временными метками.
    """
    # Переход на два уровня вверх
    root_dir: str = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
    
    # Пути к директориям
    raw_data_path: str = os.path.join(root_dir, 'data', 'raw_data')
    clear_data_path: str = os.path.join(root_dir, 'data', 'clear_data')

    # Проверка наличия директории для сохранения данных
    os.makedirs(clear_data_path, exist_ok=True)

    # Словарь для хранения данных по разным атрибутам
    data_dict: Dict[str, Dict[str, pd.Series]] = {
        'close': {},
        'open': {},
        'high': {},
        'low': {},
        'baseVolume': {},
        'quoteVolume': {},
        'numTrades': {},
        'takerBuyBaseVolume': {},
        'takerBuyQuoteVolume': {}
    }

    # Чтение и обработка файлов
    for file in tqdm(os.listdir(raw_data_path)):
        file_path: str = os.path.join(raw_data_path, file)
        data: pd.DataFrame = pd.read_csv(file_path, index_col='Unnamed: 0')
        data.index = pd.to_datetime(data['openTime'])
        ticker_name: str = file.split('.')[0]

        # Заполнение данных по каждому атрибуту
        for key in data_dict.keys():
            data_dict[key][ticker_name] = data[key]

    # Запись обработанных данных в CSV файлы
    for key, data in data_dict.items():
        output_path: str = os.path.join(clear_data_path, f'{key}.csv')
        pd.concat(data, axis=1).to_csv(output_path)


tickers_transformer()
