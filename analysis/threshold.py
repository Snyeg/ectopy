import pandas as pd


class MeanThreshold:
    
    def calculate_threshold(self, data: pd.DataFrame) -> pd.Series:
        r"""Calculate mean threshold"""
        return data.mean(axis=0)

    
class MeanNStdThreshold:
    
    def calculate_threshold(self, data: pd.DataFrame, n_std: float) -> pd.Series:
        r"""Calculate mean + n std  threshold"""
        mean = MeanThreshold().calculate_threshold(data)
        std = data.std(axis=0)
        return mean + n_std * std