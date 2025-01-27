import warnings
warnings.filterwarnings("ignore")
import numpy as np
import regex
import torch
import torch.nn as nn
from transformers import AutoTokenizer

class RegressionHead(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense1 = nn.Linear(768, 1)  # Один выход для регрессии
        
        self.dropout = nn.Dropout(p = 0.2, inplace= False)

    def forward(self, x):
        # размерности x - (batch_size = 1, seq_length = 512, hidden_size = 768)
        pooled_output = x.mean(dim=1)  # Размерность станет (batch_size, hidden_size)
        dropouted_x = self.dropout(pooled_output)
        # Пропускаем через линейный слой
        output = self.dense1(dropouted_x)  # Размерность (batch_size, 1)
        return output.squeeze(-1)  # Убираем лишнюю размерность, возвращаем (batch_size,)

class NLPModel:
    """
    Класс для работы с обученной моделью NLP
    """
    def __init__(self,
                 model_path: str,
                 tokenizer_path: str,
                 valid_tickers_list_path: str,
                 tickers_order_path: str):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, local_files_only=True)
        self.model = torch.load(model_path, map_location=device)
        self.model.eval()
        
        with open(tickers_order_path, 'r') as f:
            self.tokens_order = f.read().split()
            
        with open(valid_tickers_list_path, 'r') as f:
            self.tokens_names = set(f.read().split('\n'))
    
    def extract_tokens(self, text: str):
        return set(regex.findall(pattern="[A-Z]{3,}", string=text))&self.tokens_names
        
    def predict(self, text:str) -> np.ndarray:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        finded_tokens = self.extract_tokens(text) & self.tokens_names
        
        paragraphs = text.split('\n')
        encoded_paragraphs = self.tokenizer(paragraphs, return_tensors='pt', padding=True, truncation=True)
        
        input_ids = encoded_paragraphs['input_ids']
        input_attention_masks = encoded_paragraphs['attention_mask']
        
        input_ids = input_ids.to(device)
        input_attention_masks = input_attention_masks.to(device)
        
        sentiment = self.model(input_ids = input_ids, attention_mask = input_attention_masks).logits
        sent_mean = sentiment.mean().cpu()
        
        res = [0 for i in range(len(self.tokens_order))]
        
        if len(finded_tokens) != 0:
            for k in finded_tokens:
                for i in range(len(self.tokens_order)):
                    if k in self.tokens_order[i]:
                        res[i] = sent_mean.detach()
        else:
            res = [sent_mean.detach() for i in range(len(self.tokens_order))]
        return np.array(res)