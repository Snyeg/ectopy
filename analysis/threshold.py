import pandas as pd
import numpy as np





# === Thresholds ===

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


class PercentileThreshold(Threshold):

    _percentile: float
    
    def __init__(self, data: pd.DataFrame, percentile: float):
        super().__init__(data)
        self._percentile = percentile
    
    def calculate_threshold(self) -> pd.Series:
        return self.data.quantile(self._percentile/100.0)


class NSampleThreshold(Threshold):

    _nb_samples: int

    def __init__(self, data: pd.DataFrame, nb_samples: int):
        super().__init__(data)
        self._nb_samples = nb_samples
    
    def calculate_threshold(self, ascending=True) -> pd.Series:
        threshold = pd.Series(index=self.data.columns, dtype=float)
        for col in self.data.columns:
            threshold[col] = self.data[col].sort_values(axis=0, ascending=ascending).head(self._nb_samples).tail(1)
        return threshold


class NoiseThreshold(Threshold):
    
    _noise_level: float

    def __init__(self, data: pd.DataFrame, noise_level: float):
        super().__init__(data)
        self._noise_level = noise_level

    def calculate_threshold(self) -> pd.Series:
        return pd.Series(self._noise_level, index=self.data.columns)
 

class MaxTreshold(Threshold):

    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

    def calculate_threshold(self) -> pd.Series:
        return self.data.max()


# === Threshold Decorators ===

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




# === Adaptive threshold ===

class AdaptiveThreshold(Threshold):
    
    _noise_level: float
    _percentile: float
    _min_nb_samples: int
    _min_reference_threshold: pd.Series
    
    def __init__(self, data: pd.DataFrame, noise_level: float = 0.3, percentile: float = 15.0, 
                 min_nb_samples: int = 20, min_reference_threshold: pd.Series = None):
        super().__init__(data)
        self._noise_level = noise_level
        self._percentile = percentile
        self._min_nb_samples = min_nb_samples
        self._min_reference_threshold = min_reference_threshold
        
    def calulate_min_threshold(self):
        list_thresholds = []
        if self._percentile is not None:
            list_thresholds.append(PercentileThreshold(self.data, self._percentile).calculate_threshold())
        if self._min_nb_samples is not None:
            list_thresholds.append(NSampleThreshold(self.data, self._min_nb_samples).calculate_threshold(ascending=True))
        if self._noise_level is not None:
            list_thresholds.append(NoiseThreshold(self.data, self._noise_level).calculate_threshold())
        if self._min_reference_threshold is not None:
            list_thresholds.append(self._min_reference_threshold)
        return pd.concat(list_thresholds, axis=1).max(axis=1)

    def calulate_max_threshold(self):
        list_thresholds = []
        if self._percentile is not None:
            list_thresholds.append(PercentileThreshold(self.data, 100.0-self._percentile).calculate_threshold())
        if self._min_nb_samples is not None:
            list_thresholds.append(NSampleThreshold(self.data, self._min_nb_samples).calculate_threshold(ascending=False))
        return pd.concat(list_thresholds, axis=1).min(axis=1)
        