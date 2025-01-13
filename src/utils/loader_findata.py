import os
import csv
import pandas as pd
class finloader:
    '''
    Uploading and concatenating row-by-row data from a directory across all files and filter "USDT"
    '''
    def __init__(self,path:str):
        '''
        path - path to derectory
        '''
        self.path=path
        self.iteration_list=[]
        self.columns=[]
        for i in os.listdir(path):
            self.iteration_list.append(csv.reader(open(path+"/"+i)))
            self.columns+=list(map(lambda x: i[:-4]+"_"+x,next(self.iteration_list[-1])[1:]))
        self.h=list(map(lambda x: x[-4:]=="USDT", self.columns))
        self.columns=["date"]+list(filter(lambda x: x[-4:]=="USDT", self.columns))
        pass
    def step(self):
        '''
        do step and return DataFrame - next concatination object
        '''
        lst=[]
        fl=False
        for i in self.iteration_list:
            try:
                if fl:
                    k=next(i)[1:]
                    for j in range(len(k)):
                        if(self.h[j]):
                            lst+=[k[j]]
                else:
                    k=next(i)
                    lst+=[k[0]]
                    for j in range(len(k)-1):
                        if(self.h[j]):
                            lst+=[k[j+1]]
                    fl=True
            except:
                return None
        return pd.DataFrame(columns=self.columns[1:],data=[lst[1:]], index=[lst[0]])
    def __len__(self):
        '''
        return count row
        '''
        return len(pd.read_csv(self.path+"/"+os.listdir(self.path)[0]))
    def close(self):
        '''
        close all files
        '''
        path=self.path
        self.iteration_list=[]
        for i in os.listdir(path):
            self.iteration_list.append(csv.reader(open(path+"/"+i)))
            next(self.iteration_list[-1])
        for i in os.listdir(path):
            open(path+"/"+i).close()
        pass