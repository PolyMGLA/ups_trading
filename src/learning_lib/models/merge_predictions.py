import numpy as np
import pandas as pd

COEF = 0.99
ALP = 1.0

def neutralize(alpha):
    return alpha.sub(
        alpha.mean(axis=1),
        axis=0
    )

def scale(alpha):
    return alpha.div(
        alpha
        .abs()
        .sum(axis=1),
        axis=0
    )

class PredictionMerger:
    def __init__(self):        
        self.news = np.array([.0 for i in range(120)], dtype=np.float32)
        
    def merge(self,
              predictions_fin: np.ndarray,
              predictions_news: np.ndarray) -> np.ndarray:
        self.news = self.news * COEF + predictions_news
        return scale(
            neutralize(
                pd.DataFrame([predictions_fin * ALP + self.news * (1 - ALP)], columns=list(range(120)))
                )
            ).to_numpy()