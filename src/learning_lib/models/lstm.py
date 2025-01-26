import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
import pandas as pd

class CustomLoss2(nn.Module):
    def __init__(self):
        super(CustomLoss2, self).__init__()

    def forward(self, input, target):
        # Compute the loss

        alpha = normalize_tensor(neutralize_tensor(input))
        return -(torch.mul(alpha, target).sum())/torch.sum(torch.mul(alpha, target),1).std()#*((input-target).abs().mean()**(-1))
def neutralize_tensor(alpha):
    return torch.sub(alpha.T,torch.mean(alpha,1)).T

def normalize_tensor(alpha):
    return torch.div(alpha.T,torch.sum(alpha.abs(),1)).T

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

def train_pipeline(epochs: int, criterion, optimizer, model, epochs_period: int, X, Y):
    trainX,testX,trainY,testY=train_test_split(X,Y,shuffle=False,test_size=2000)
    X_train_tensors_final=torch.tensor(np.array(trainX),dtype=torch.float32).to('cuda')
    Y_train_tensors_final=torch.tensor(np.array(trainY),dtype=torch.float32).to('cuda')
    X_test_tensors_final=torch.tensor(np.array(testX),dtype=torch.float32).to('cuda')
    Y_test_tensors_final=torch.tensor(np.array(testY),dtype=torch.float32).to('cuda')
    metr_best=1000000000
    for epoch in range(epochs):
        model.train()
        outputs = model.forward(X_train_tensors_final) #forward pass
        optimizer.zero_grad() #caluclate the gradient, manually setting to 0
        loss = criterion(outputs, Y_train_tensors_final)
        loss.backward() #calculates the loss of the loss function
        optimizer.step() #improve from loss, i.e backprop

        if epoch % epochs_period == 0:
            model.eval()
            val_outputs = model(X_test_tensors_final)
            metr = criterion(val_outputs.detach(),Y_test_tensors_final.detach())
            print(metr)
            if metr<metr_best:
                torch.save(model.state_dict(),"param_model.pth")
                metr_best=metr
            model.train()
class MYLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim):
        super(MYLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.layer_dim = layer_dim
        self.lstm = nn.LSTM(input_dim, hidden_dim, layer_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 128)
        self.dr=nn.Dropout(p=0.7)
        self.fc2=nn.Linear(128,128)
        self.fc3=nn.Linear(128,output_dim)

    def forward(self, x, h0=None, c0=None):
        # If hidden and cell states are not provided, initialize them as zeros
        if h0 is None or c0 is None:
            h0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).to(x.device)
            c0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).to(x.device)
        
        # Forward pass through LSTM
        out, (hn, cn) = self.lstm(x, (h0, c0))
        out=out[:, -1, :]
        out=self.dr(out)
        out = self.fc(out)  # Selecting the last output
        out=self.dr(out)
        out=self.fc2(out)
        out=self.dr(out)
        out=self.fc3(out)
        return out
class LSTMModel:
    """
    Класс для работы с обученной LSTM-моделью
    """
    def __init__(self,NUM_LAYERS=10, INPUT_SIZE=1080, NUM_TICKERS=120):
        self.__NUM_LAYERS=NUM_LAYERS
        self.__INPUT_SIZE=INPUT_SIZE
        self.__NUM_TICKERS=NUM_TICKERS
        self.__HIDDEN_SIZE=100
        pass

    def predict(self,X) -> np.ndarray:
        model=MYLSTM(output_dim=self.__NUM_TICKERS, input_dim=self.__INPUT_SIZE, hidden_dim=self.__HIDDEN_SIZE, layer_dim=self.__NUM_LAYERS).to('cuda') #our lstm class
        model.load_state_dict(torch.load("param_model.pth",weights_only=True))
        model.eval()
        return model(torch.tensor([X.values],dtype=torch.float32).to("cuda")).to('cpu').detach().numpy()[0]
    
    def retrain(self,X,HIDDEN_SIZE:int=100,LEARNING_RATE:float =0.0001):
        INPUT_SIZE = self.__INPUT_SIZE #number of features
        NUM_LAYERS = self.__NUM_LAYERS #number of stacked lstm layers
        NUM_CLASSES = self.__NUM_TICKERS #number of output classes
        self.__HIDDEN_SIZE=HIDDEN_SIZE 
        MODEL = MYLSTM(output_dim=NUM_CLASSES, input_dim=INPUT_SIZE, hidden_dim=HIDDEN_SIZE, layer_dim=NUM_LAYERS).to('cuda') #our lstm class
        EPOCHS = 2500 #1000 epochs
        LEARNING_RATE = 0.0001 #0.001 lr
        CRITERION = CustomLoss2().to('cuda')
        OPTIMIZER = torch.optim.Adam(MODEL.parameters(), lr = LEARNING_RATE)
        Y=(X[list(filter(lambda x: x[:5]=='close', list(X.columns)))][self.__NUM_LAYERS-1:].shift(-1)/X[list(filter(lambda x: x[:5]=='close', list(X.columns)))][self.__NUM_LAYERS-1:]).iloc[:-1]
        prepro2=torch.load("std_sclr.bin")
        df2=pd.DataFrame(prepro2.transform(X))
        df3=[]
        for i in range(self.__NUM_LAYERS, len(df2)):
            df3.append(np.array(df2.iloc[i-self.__NUM_LAYERS: i]))
        train_pipeline(epochs=EPOCHS,criterion=CRITERION, optimizer=OPTIMIZER, model=MODEL.to('cuda'), epochs_period=10,X=df3, Y=Y)

        
        
