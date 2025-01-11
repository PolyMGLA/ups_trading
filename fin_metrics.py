import numpy as np

def PnL(x):
    '''x here it is alpha*returns'''
    return x.sum().sum()
def Sharpe(x):
    return PnL(x) / x.sum(axis=1).std()
def Drawdown(x):
    pnl_vector = x.sum(axis=1)
    return max((pnl_vector.cummax() - pnl_vector.cumsum()) / pnl_vector.cummax())
def Turnover(alpha):
    turnovers = []
    for i in range(1, len(alpha)):
        turnovers.append((alpha.iloc[i] - alpha.iloc[i-1]).abs().sum())
    return np.array(turnovers).mean()
def Turnovers_distribution(alpha):
    turnovers = []
    for i in range(1, len(alpha)):
        turnovers.append((alpha.iloc[i] - alpha.iloc[i-1]).abs().sum())
    return np.array(turnovers)
def Get_metrics(x,alpha):
    return {"Pnl": PnL(x), "Sharpe": Sharpe(x), "Drawdown": Drawdown(x), "Turnover": Turnover(alpha)}