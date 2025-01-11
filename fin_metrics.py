import numpy as np
import pandas as pd

class FinCalculations:
    '''
    class for calculating results of alpha strategy
    '''
    @staticmethod
    def pnl_vec(
        alpha: pd.DataFrame,
        returns: pd.DataFrame    
    ) -> pd.Series:
        '''
        func to calculate pnl by alpha & returns
        '''
        return (alpha * returns).sum(axis=1)
    
    def pnl(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> float:
        '''
        func to calculate final pnl by alpha & returns
        '''
        return FinCalculations.pnl_vec(alpha, returns).sum()
    
    @staticmethod
    def sharpe(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> pd.Series:
        '''
        func to calculate sharpe by alpha & returns
        '''
        return FinCalculations.pnl(alpha, returns).sum() / FinCalculations.pnl(alpha, returns).std()
    
    @staticmethod
    def drawdown_vec(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> pd.Series:
        '''
        func to calculate drawdown_vec by alpha & returns
        '''
        return (
            FinCalculations.pnl(alpha, returns).cummax() - \
            FinCalculations.pnl(alpha, returns).cummax()
        ) / (
            FinCalculations.pnl(alpha, returns).cummax() + 1
        )
    
    def maxDrawdown(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> float:
        '''
        func to calculate max drawdown by alpha & returns
        '''
        return FinCalculations.drawdown_vec(alpha, returns).max()

    def turnover_vec(
        alpha: pd.DataFrame
    ) -> pd.Series:
        '''
        func to calculate mean turnover
        '''
        return (alpha - alpha.shift()).abs().sum(axis=1)
    
    def turnover(
        alpha: pd.DataFrame
    ) -> float:
        '''
        func to calculate turnover vector
        '''
        return FinCalculations.turnover_vec(alpha).mean()

    def metrics(
        alpha: pd.DataFrame,
        returns: pd.DataFrame
    ) -> pd.DataFrame:
        '''
        func to calculate all metrics
        '''
        metrics_dict = {}
        metrics_dict["Pnl"] = FinCalculations.pnl(alpha)
        metrics_dict["Sharpe"] = FinCalculations.sharpe(alpha, returns)
        metrics_dict["Max Drawdown"] = FinCalculations.maxDrawdown(alpha, returns)
        metrics_dict["Turnover"] = FinCalculations.turnover(alpha)
        return pd.DataFrame(metrics_dict, index=[0])