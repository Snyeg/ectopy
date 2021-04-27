import numpy as np
import pandas as pd


class Threshold:
    def __init__(self, data):
        self.data = data
    def calculate_threshold(self):
        pass
        
class MeanTreshold(Threshold):
    def __init__(self, data):
        super().__init__(data)
        self.mean = data.mean(axis=0)
        self.std = data.std(axis=0)
        
    def calculate_threshold(self, data, nb_std = 0):
        return self.mean
        
class ThresholdDecorator(Threshold):
    def __init__(self, treshold: Threshold):
        self.treshold = treshold
        
    
    @property
    def meanTreshold(self):
        return self.meanTreshold
        
    def calculate_threshold(self, data, nb_std = 0):
        return self.mean     

class MeanNStdThreshold(ThresholdDecorator):
    def __init__(self, data):
        super().__init__(data)

    def calculate_threshold(self, data, nb_std):
        return data.mean + nb_std * data.std
        

df = pd.DataFrame(np.random.randint(0, 2, size=(5, 4)), columns=list('ABCD'))

f = MeanNStdThreshold(MeanTreshold(df))
f.calculate_threshold(MeanTreshold(df),5))
    
    

