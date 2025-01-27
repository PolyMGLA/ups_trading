import numpy as np
from threading import Thread
from .fin_metrics import FinCalculations
import json
import torch as pt
import pandas as pd

class StrategyUpdater:
    folder_path = ""
    def __init__(self,
                 folder_path: str = "src/frontend/src/lib/data") -> None:
        self.folder_path = folder_path

    @staticmethod
    def to_pd(vec: np.ndarray) -> pd.DataFrame:
        return pd.DataFrame(vec)

    def update(self,
               alpha: np.ndarray,
               returns: np.ndarray) -> None:
        print("alpha =", alpha.shape)
        print("returns =", returns.shape)
        # print(alpha)
        # print(returns)
        alpha = self.to_pd(alpha)
        returns = self.to_pd(returns)
        print(FinCalculations.metrics_dict(alpha, returns))
        with open(f"{self.folder_path}/metrics.json", "w") as f:
            json.dump(
                FinCalculations.metrics_dict(alpha, returns),
                f, indent=4)