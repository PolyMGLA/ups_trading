import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

from utils.windowed_learning_pipeline import Windowed_learning_pipeline

# Set random seed for reproducibility
np.random.seed(0)
torch.manual_seed(0)

pipeline = Windowed_learning_pipeline(
    _pth = "./src/data/",
    _train_size = 300000,
    _dropout_size = 2000,
    _win_size = 20000,
    _win_train_size = 15000
)

class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim):
        super(LSTMModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.layer_dim = layer_dim
        self.lstm = nn.LSTM(input_dim, hidden_dim, layer_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, h0=None, c0=None):
        # If hidden and cell states are not provided, initialize them as zeros
        if h0 is None or c0 is None:
            print(x)
            h0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).to(x.device)
            c0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).to(x.device)
        
        # Forward pass through LSTM
        out, (hn, cn) = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])  # Selecting the last output
        return out, hn, cn
    
model = LSTMModel(input_dim=960, hidden_dim=100, layer_dim=1, output_dim=120)
criterion = nn.L1Loss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop
num_epochs = 100
h0, c0 = None, None  # Initialize hidden and cell states

def create_dataset(dataset: np.ndarray, lookback: int, predict_size: int):
    """принимает numpy-array и превращает его в датасет для обучения LSTM
    
    Args:
        dataset: нампай массив с данными для обучения
        lookback: размер исторических данных для предсказания
        predict_size: сколько значений вперёд предсказываем

    Returns:
        X, y: np.ndarray где X - входные данные, y - целевые

    """
    X, y = [], [] #создадим массивы входных и целевых данных
    i = 0
    while True: #Нарежем
        if i + lookback + predict_size > len(dataset):
            break
        feature = dataset[i:i + lookback]
        target = dataset[i + lookback:i + lookback + predict_size]
        X.append(feature)
        y.append(target)
        i += lookback
    return torch.tensor(X, dtype=torch.float64), torch.tensor(y, dtype=torch.float64)

window = pipeline.get_nxt()

while window is not None:
    train, test = window
    train = train.to_numpy()
    test = test.to_numpy()
    trainX, trainY = create_dataset(train, 1000, 400)
    print(trainX)

    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()

        # Forward pass
        outputs, h0, c0 = model(trainX, h0, c0)

        # Compute loss
        loss = criterion(outputs, trainY)
        loss.backward()
        optimizer.step()

        # Detach hidden and cell states to prevent backpropagation through the entire sequence
        h0 = h0.detach()
        c0 = c0.detach()

        if (epoch+1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
    
    window = pipeline.get_nxt()