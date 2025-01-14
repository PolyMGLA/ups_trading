import numpy as np
import pandas as pd

class FinCalculations:
    '''
    Класс для вычисления результатов альфа-стратегии.
    Содержит методы для расчета доходности (PnL), коэффициента Шарпа, максимальной просадки и других метрик.
    '''

    @staticmethod
    def pnl_vec(
        alpha: pd.DataFrame,
        returns: pd.DataFrame    
    ) -> pd.Series:
        '''
        Метод для расчета вектора доходности (PnL) по альфе и доходности активов.
        Альфа умножается на доходность для получения доходности по каждому активу.
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :param returns: Датафрейм с доходностью активов.
        :return: Серия с результатами доходности по каждому временному интервалу.
        '''
        return (alpha * returns).sum(axis=1)
    
    @staticmethod
    def pnl(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> float:
        '''
        Метод для расчета общего значения доходности (PnL).
        Суммируется весь результат из вектора доходности (PnL).
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :param returns: Датафрейм с доходностью активов.
        :return: Финальное значение PnL.
        '''
        return FinCalculations.pnl_vec(alpha, returns).sum()
    
    @staticmethod
    def sharpe(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> pd.Series:
        '''
        Метод для расчета коэффициента Шарпа.
        Он вычисляется как отношение средней доходности (PnL) к стандартному отклонению доходности (PnL).
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :param returns: Датафрейм с доходностью активов.
        :return: Коэффициент Шарпа для данной альфа-стратегии.
        '''
        return FinCalculations.pnl(alpha, returns).sum() / FinCalculations.pnl(alpha, returns).std()
    
    @staticmethod
    def drawdown_vec(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> pd.Series:
        '''
        Метод для расчета вектора просадки (drawdown).
        Просадка вычисляется как разница между текущим пиком накопленной доходности и текущей доходностью.
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :param returns: Датафрейм с доходностью активов.
        :return: Вектор просадок для каждого временного интервала.
        '''
        return (
            FinCalculations.pnl(alpha, returns).cummax() - \
            FinCalculations.pnl(alpha, returns)
        ) / (
            FinCalculations.pnl(alpha, returns).cummax() + 1
        )
    
    @staticmethod
    def maxDrawdown(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> float:
        '''
        Метод для расчета максимальной просадки.
        Выбирается максимальное значение из вектора просадок.
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :param returns: Датафрейм с доходностью активов.
        :return: Максимальная просадка.
        '''
        return FinCalculations.drawdown_vec(alpha, returns).max()

    @staticmethod
    def turnover_vec(
        alpha: pd.DataFrame
    ) -> pd.Series:
        '''
        Метод для расчета изменения (turnover) весов стратегии.
        Изменение веса вычисляется как разница между текущими весами альфы и весами на предыдущем шаге.
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :return: Серия изменений весов по каждому временному интервалу.
        '''
        return (alpha - alpha.shift()).abs().sum(axis=1)
    
    @staticmethod
    def turnover(
        alpha: pd.DataFrame
    ) -> float:
        '''
        Метод для расчета среднего изменения весов стратегии.
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :return: Среднее изменение (turnover) весов стратегии.
        '''
        return FinCalculations.turnover_vec(alpha).mean()
    
    @staticmethod
    def decay(
        alpha: pd.DataFrame,
        win: int
    ) -> pd.DataFrame:
        '''
        Метод для расчета decay с экспоненциальным сглаживанием.
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :param win: Параметр окна для экспоненциального сглаживания.
        :return: Альфа после сглаживания.
        '''

        return alpha.ewm(span=win).mean() 
    
    @staticmethod
    def profit_margin(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> float:
        '''
        Метод для расчета метрики Profit Margin.

        :param alpha: Датафрейм с весами альфа-стратегии.
        :param returns: Датафрейм с доходностью активов.
        :return: Значение Profit Margin.
        '''
        pnl = FinCalculations.pnl_vec(alpha, returns)
        tvr = FinCalculations.turnover_vec(alpha)
        return pnl.mean() / tvr.mean() if tvr.mean() != 0 else np.nan

    @staticmethod
    def metrics(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> pd.DataFrame:
        '''
        Метод для расчета всех основных метрик альфа-стратегии:
        - Доходность (PnL)
        - Коэффициент Шарпа
        - Максимальная просадка
        - Оборот (turnover)
        
        :param alpha: Датафрейм с весами альфа-стратегии.
        :param returns: Датафрейм с доходностью активов.
        :return: Датафрейм с рассчитанными метриками.
        '''
        metrics_dict = {}
        metrics_dict["Pnl"] = FinCalculations.pnl(alpha, returns)
        metrics_dict["Sharpe"] = FinCalculations.sharpe(alpha, returns)
        metrics_dict["Max Drawdown"] = FinCalculations.maxDrawdown(alpha, returns)
        metrics_dict["Turnover"] = FinCalculations.turnover(alpha)
        return pd.DataFrame([metrics_dict])
