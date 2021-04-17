import pandas as pd

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




