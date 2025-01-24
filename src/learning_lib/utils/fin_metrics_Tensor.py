import numpy as np
import pandas as pd
import torch as pt

class FinCalculationsTensor:
    '''
    Класс для вычисления результатов альфа-стратегии.
    Содержит методы для расчета доходности (PnL), коэффициента Шарпа, максимальной просадки и других метрик.
    '''

    @staticmethod
    def pnl_tensor(
        alpha: pt.tensor,
        returns: pt.tensor    
    ) -> pt.tensor:
        '''
        Метод для расчета вектора доходности (PnL) по альфе и доходности активов.
        Альфа умножается на доходность для получения доходности по каждому активу.
        
        :param alpha: tensor с весами альфа-стратегии.
        :param returns: tensor с доходностью активов.
        :return: tensor с результатами доходности по каждому временному интервалу.
        '''
        return pt.multiply(alpha, returns).sum(dim=1)
    
    @staticmethod
    def pnl(
        alpha: pt.tensor,
        returns: pt.tensor
    ) -> pt.tensor:
        '''
        Метод для расчета общего значения доходности (PnL).
        Суммируется весь результат из вектора доходности (PnL).
        
        :param alpha: tensor с весами альфа-стратегии.
        :param returns: tensor с доходностью активов.
        :return: Финальное значение PnL.
        '''
        return FinCalculationsTensor.pnl_tensor(alpha, returns).sum(dim=0)
    
    @staticmethod
    def sharpe(
        alpha: pt.tensor,
        returns: pt.tensor
    ) -> pt.tensor:
        '''
        Метод для расчета коэффициента Шарпа.
        Он вычисляется как отношение средней доходности (PnL) к стандартному отклонению доходности (PnL).
        
        :param alpha: tensor с весами альфа-стратегии.
        :param returns: tensor с доходностью активов.
        :return: Коэффициент Шарпа для данной альфа-стратегии.
        '''
        return pt.multiply(alpha, returns).sum() / pt.multiply(alpha, returns).std()
    
    @staticmethod
    def drawdown_tensor(
        alpha: pt.tensor,
        returns: pt.tensor
    ) -> pt.tensor:
        '''
        Метод для расчета вектора просадки (drawdown).
        Просадка вычисляется как разница между текущим пиком накопленной доходности и текущей доходностью.
        
        :param alpha: tensor с весами альфа-стратегии.
        :param returns: tensor с доходностью активов.
        :return: tensor просадок для каждого временного интервала.
        '''
        return (
            FinCalculationsTensor.pnl_tensor(alpha, returns).cummax() - \
            FinCalculationsTensor.pnl_tensor(alpha, returns)
        ) / (
            FinCalculationsTensor.pnl_tensor(alpha, returns).cummax() + 1
        )
    
    @staticmethod
    def maxDrawdown(
        alpha: pt.tensor,
        returns: pt.tensor
    ) -> pt.tensor:
        '''
        Метод для расчета максимальной просадки.
        Выбирается максимальное значение из вектора просадок.
        
        :param alpha: tensor с весами альфа-стратегии.
        :param returns: tensor с доходностью активов.
        :return: Максимальная просадка.
        '''
        return FinCalculationsTensor.drawdown_vec(alpha, returns).max()

    @staticmethod
    def turnover_tensor(
        alpha: pt.tensor
    ) -> pt.tensor:
        '''
        Метод для расчета изменения (turnover) весов стратегии.
        Изменение веса вычисляется как разница между текущими весами альфы и весами на предыдущем шаге.
        
        :param alpha: tensor с весами альфа-стратегии.
        :return: tensor изменений весов по каждому временному интервалу.
        '''
        alpha1=pd.DataFrame(alpha.numpy())
        return pt.tensor((alpha1 - alpha1.shift()).abs().sum(axis=1))
    
    @staticmethod
    def turnover(
        alpha: pt.tensor
    ) -> float:
        '''
        Метод для расчета среднего изменения весов стратегии.
        
        :param alpha: tensor с весами альфа-стратегии.
        :return: Среднее изменение (turnover) весов стратегии.
        '''
        return FinCalculationsTensor.turnover_vec(alpha).mean()
    
    @staticmethod
    def decay(
        alpha: pt.tensor,
        win: int
    ) -> pt.tensor:
        '''
        Метод для расчета decay с экспоненциальным сглаживанием.
        
        :param alpha: tensor с весами альфа-стратегии.
        :param win: Параметр окна для экспоненциального сглаживания.
        :return: Альфа после сглаживания.
        '''
        alpha1=pd.DataFrame(alpha.numpy())
        return pt.tensor(alpha1.ewm(span=win).mean())
    
    @staticmethod
    def profit_margin(
        alpha: pt.tensor,
        returns: pt.tensor
    ) -> pt.tensor:
        '''
        Метод для расчета метрики Profit Margin.

        :param alpha: tensor с весами альфа-стратегии.
        :param returns: tensor с доходностью активов.
        :return: Значение Profit Margin.
        '''
        pnl = FinCalculationsTensor.pnl_vec(alpha, returns)
        tvr = FinCalculationsTensor.turnover_vec(alpha)
        return pnl.mean() / tvr.mean() if tvr.mean() != 0 else np.nan

    @staticmethod
    def metrics(
        alpha: pt.tensor,
        returns: pt.tensor
    ) -> pt.tensor:
        '''
        Метод для расчета всех основных метрик альфа-стратегии:
        - Доходность (PnL)
        - Коэффициент Шарпа
        - Максимальная просадка
        - Оборот (turnover)
        
        :param alpha: tensor с весами альфа-стратегии.
        :param returns: tensor с доходностью активов.
        :return: tensor с рассчитанными метриками.
        '''
        metrics_dict = {}
        metrics_dict["Pnl"] = FinCalculationsTensor.pnl(alpha, returns)
        metrics_dict["Sharpe"] = FinCalculationsTensor.sharpe(alpha, returns)
        metrics_dict["Max Drawdown"] = FinCalculationsTensor.maxDrawdown(alpha, returns)
        metrics_dict["Turnover"] = FinCalculationsTensor.turnover(alpha)
        return pd.DataFrame([metrics_dict])
