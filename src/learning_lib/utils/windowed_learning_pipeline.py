import datetime
from collections import deque

import tqdm
from .loader_findata import Finloader
import pandas as pd
import numpy as np
class Windowed_learning_pipeline:
    def __init__(self,
                 _pth: str,
                 _train_size: int,
                 _dropout_size: int,
                 _win_size: int,
                 _win_train_size: int):
        '''
        С помощью метода get_next() выдаёт следующее скользящее окно для обучения LSTM сети
        Аргументы:
        - _pth: путь к 9 csv файлам с рыночными данными
        - _train_size: размер тренировочной выборки
        - _dropout_size: размер выбрасываемых значений
        - _win_size: размер окна
        - _win_train_size: 
        

        Порядок работы:
        get_test() нужное число раз -> drop_dropout() -> get_test()
        '''

        self.train_size = _train_size
        self.data = Finloader(_pth)
        self.length = len(self.data)
        self.dropout_size = _dropout_size
        self.win_size = _win_size
        self.win_train_size = _win_train_size
        self.dropout_flag = 0
        self.columns = self.data.get_columns()
        self.getted_cnt = 0

        self.start_batch = 0

        self.win = deque()
        self.win_time = deque()

    def get_test(self):
        '''Возвращает тестовую выборку test:pd.DataFrame. Если окна и дропаут не сброшены - возвращает None.'''
        if not self.dropout_flag or self.getted_cnt == self.length:
            return None
        else:
            test_dat = []
            test_time = []
            for i in tqdm.tqdm(range(self.getted_cnt, self.length)):
                dat, time = self.data.step()
                self.getted_cnt +=1
                test_dat.append(dat)
                test_time.append(time)
            df_test = pd.DataFrame(data = test_dat,
                                index = test_time,
                                columns=self.columns)
            
            df_test=df_test.ffill()
            
            return df_test
    
    def drop_dropout(self):
        '''Сбрасывает дропаут (данные между окнами и тестом). Если уже сброшены - вернёт None.'''
        if self.dropout_flag == 1:
            return None
        self.dropout_flag = 1
        print("Удаление дропаута...")
        for i in tqdm.tqdm(range(self.dropout_size)):
            self.getted_cnt += 1
            self.data.step()
    
    def get_nxt(self):
        '''Получить следующие train и test, если вся выборка выгружена вернёт None
            Возвращает (train:pd.DataFrame, test:pd.DataFrame)
        '''
        if self.dropout_flag:
            raise "NotImplementedError"
        
        if self.getted_cnt + self.win_size - self.win_train_size >= self.train_size:
            return None
        
        if self.getted_cnt == 0:
            for i in tqdm.tqdm(range(self.win_size)):
                cur_time, cur_dat = self.data.step()
                self.getted_cnt += 1
                self.win.append(cur_dat)
                self.win_time.append(cur_time)
            print("first iteration OK")
        else:
            for i in tqdm.tqdm(range(self.win_size - self.win_train_size)):
                cur_time, cur_dat = self.data.step()
                self.getted_cnt += 1

                self.win.popleft()
                self.win_time.popleft()

                self.win.append(cur_dat)
                self.win_time.append(cur_time)

        win_list = list(self.win)
        time_list = list(self.win_time)

        train_dat, test_dat = win_list[:self.train_size], win_list[self.win_size:]
        train_time, test_time = time_list[:self.train_size], time_list[self.win_size:]

        df_train = pd.DataFrame(data = train_dat,
                                index = train_time,
                                columns=self.columns)
        
        df_test = pd.DataFrame(data = test_dat,
                                index = test_time,
                                columns=self.columns)
        
        df_train = df_train.ffill()
        df_test = df_test.ffill()
        
        return (df_train, df_test)