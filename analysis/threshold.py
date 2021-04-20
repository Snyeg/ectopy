import pandas as pd
import numpy as np

class Threshold:
     """Abstract threshold class"""

     _data: pd.DataFrame

     def __init__(self, data: pd.DataFrame):
         self._data = data

     @property
     def data(self) -> pd.DataFrame:
         return self._data

     def calculate_threshold(self) -> pd.Series:
         pass


class MeanTreshold(Threshold):

     def __init__(self, data: pd.DataFrame):
         super().__init__(data)

     def calculate_threshold(self) -> pd.Series:
         return self.data.mean()

class PourcentilesAdptativeThreshold(Threshold):

      def __init__(self, data: pd.DataFrame, pourcentiles: float):
         super().__init__(data)
         self.min_threshold = data.sort_values(by=list(data.columns)).quantile(pourcentiles/100)
         self.max_threshold = data.sort_values(by=list(data.columns)).quantile((100-pourcentiles)/100)

class NSamplesAdptativeThreshold(Threshold):

      def __init__(self, data: pd.DataFrame, nb_samples: int):
         super().__init__(data)
         self.min_threshold = data.sort_values(by=list(data.columns)).head(nb_samples).tail(1)
         self.max_threshold = data.sort_values(by=list(data.columns)).tail(nb_samples).head(1)

class MaxTreshold(Threshold):

     def __init__(self, data: pd.DataFrame):
         super().__init__(data)

     def calculate_threshold(self) -> pd.Series:
         return self.data.max()


class ThresholdDecorator(Threshold):
     """Abstract threshold decorator class"""

     _threshold: Threshold

     def __init__(self, threshold: Threshold):
         self._threshold = threshold

     @property
     def threshold(self) -> pd.Series:
         return self._threshold

     def calculate_threshold(self) -> pd.Series:
         pass


class StdDecorator(ThresholdDecorator):

     _nb_std: float

     def __init__(self, threshold: Threshold, nb_std: float = 0.0):
         super().__init__(threshold)
         self._nb_std = nb_std

     @property
     def nb_std(self) -> float:
         return self._nb_std

     def calculate_threshold(self) -> pd.Series:
         return self.threshold.data.mean() + self.nb_std * self.threshold.data.std()
     
class MaxNormalDataDecorator(ThresholdDecorator):

     _data_normal_max: float
     _min_threshold: float

     def __init__(self, threshold: Threshold, data_normal: pd.DataFrame, min_threshold: float):
         super().__init__(threshold)
         self._data_normal_max = data_normal.max()
         self._min_threshold = min_threshold

     @property
     def data_normal_max(self) -> float:
         return self._data_normal_max
     @property
     def min_threshold(self) -> float:
         return self._min_threshold

     def calculate_threshold(self) -> pd.Series:
         return np.maximum(self.min_threshold,self.data_normal_max)



df = pd.DataFrame(np.random.randint(0,100,size=(100, 1)), columns=["G1"])
df=df/100

data = pd.DataFrame(np.random.randint(0,15,size=(100, 1)), columns=["G1"])
data=data/100


n_samples_thresold = NSamplesAdptativeThreshold(df,20)

print(n_samples_thresold.min_threshold)
print(n_samples_thresold.max_threshold)

pourcentiles_thresold = PourcentilesAdptativeThreshold(df,15)
max_pourcentiles_threshold = MaxNormalDataDecorator(pourcentiles_thresold, data, pourcentiles_thresold.min_threshold)

print(pourcentiles_thresold.min_threshold)
print(pourcentiles_thresold.max_threshold)
print(max_pourcentiles_threshold.calculate_threshold())

