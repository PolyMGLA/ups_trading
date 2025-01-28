import numpy as np
from threading import Thread
from .fin_metrics import FinCalculations
import json
import torch as pt
import pandas as pd

class StrategyUpdater:
    folder_path = ""
    pnl = []
    def __init__(self,
                 folder_path: str = "src/frontend/src/lib/data") -> None:
        self.folder_path = folder_path

    @staticmethod
    def to_pd(vec: np.ndarray) -> pd.DataFrame:
        return pd.DataFrame(vec)

    def update(self,
               alpha: np.ndarray,
               returns: np.ndarray,
               tick: list[str]) -> None:
        print("alpha =", alpha.shape)
        print("returns =", returns.shape)
        aa = alpha.copy()
        # print(alpha)
        # print(returns)
        alpha = self.to_pd(alpha)
        returns = self.to_pd(returns)
        print(FinCalculations.metrics_dict(alpha, returns))
        with open(f"{self.folder_path}/metrics.json", "w") as f:
            json.dump(
                FinCalculations.metrics_dict(alpha, returns),
                f, indent=4)
        self.pnl = self.pnl[-10:]
        self.pnl.append(round(FinCalculations.pnl(alpha, returns), 2))
        with open(f"{self.folder_path}/income.json", "w") as f:
            json.dump(
                [list(range(len(self.pnl))), self.pnl],
                f, indent=4
            )
        with open(f"{self.folder_path}/allocation.json", "w") as f:
            json.dump(
                [tick, list(map(abs, aa[-1]))],
                f, indent=4
            )