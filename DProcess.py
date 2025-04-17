import pandas as pd
import numpy as np
import os

class DataProcess():
    def __init__(self):

        # if data exist, flag true
        self.__flag = False
        self.__data = None
        self.__path = None
        pass

    def openFile(self, path):
        self.__path = path
        if os.path.isfile(self.__path):
            self.__flag = True
            self.__data = pd.read_csv(path).loc[:,["antecedents","consequents","oddsratio"]].to_numpy()
        else:
            print("invalid url")
            self.__flag = False
        
    def selectAnt(self, anstecedents_ = "all", source_ = "data"):
        if(self.__flag):
            try:
                if source_ == "data":
                    source_ = self.__data
            except:
                pass
            if(anstecedents_=='all'):
                return source_
            elif(anstecedents_=="none"):
                return None
            else:
                temp = []
                for i in range(source_.shape[0]):
                    if source_[i,0] == anstecedents_:
                        temp.append(i)
                data = np.array([source_[i] for i in temp])
                return data
        else:
            print("invalid operation")
            return None
    
    def selectCon(self, consequences_ = "all", source_ = "data"):
        if(self.__flag):
            try:
                if source_ == "data":
                    source_ = self.__data
            except :
                pass
            if(consequences_=='all'):
                return source_
            elif(consequences_=="none"):
                return None
            else:
                temp = []
                for i in range(source_.shape[0]):
                    if source_[i,1] == consequences_:
                        temp.append(i)
                data = np.array([source_[i] for i in temp])
                return data
        else:
            print("invalid operation")
            return None

    def get_path(self):
        return self.__path
