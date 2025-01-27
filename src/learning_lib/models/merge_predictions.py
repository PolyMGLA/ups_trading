import numpy as np

COEF = 0.99
ALP = 0.5

class PredictionMerger:
    def __init__(self):        
        self.news = np.array([.0 for i in range(120)], dtype=np.float32)
        
    def merge(self,
              predictions_fin: np.ndarray,
              predictions_news: np.ndarray) -> np.ndarray:
        self.news = self.news * COEF + predictions_news
        return predictions_fin * ALP + self.news * (1 - ALP)