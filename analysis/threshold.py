import pandas as pd
import numpy as np
from lifelines import CoxPHFitter


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
    
    def get_threshold_percentile(self, expression_values: pd.Series, threshold: float) -> float:
        values = expression_values.sort_values().to_numpy()
        if (len(values)==0.0):
            return 0.0
        n = 0
        for i in range(len(values)):
            if (values[i]<=threshold):
                n = n + 1
        return 100.0 * n / len(values)


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
        return self.threshold.calculate_threshold() + self.nb_std * self.threshold.data.std()




# === Adaptive threshold ===

class AdaptiveThreshold(Threshold):
    
    _survival_data: pd.DataFrame
    _duration_col: str
    _event_col: str
    
    _noise_level: float
    _percentile: float
    _step_percentile: float
    _min_nb_samples: int
    _min_reference_threshold: pd.Series
    
    _min_threshold: pd.Series
    _max_threshold: pd.Series
    
    _eligible_features: list
    _dict_thresholds: dict # {'gene' : pd.DataFrame('thresholds', 'threshold_percentiles')} 
    
    def __init__(
            self, 
            data: pd.DataFrame,
            survival_data: pd.DataFrame, 
            duration_col: str = 'time', 
            event_col:str = 'event', 
            noise_level: float = 0.3, 
            percentile: float = 15.0, 
            step_percentile: float = 1.0, 
            min_nb_samples: int = 20, 
            min_reference_threshold: pd.Series = None
            ):
        
        super().__init__(data)
        self._survival_data = survival_data
        self._duration_col = duration_col
        self._event_col = event_col
        self._noise_level = noise_level
        self._percentile = percentile
        self._step_percentile = step_percentile
        self._min_nb_samples = min_nb_samples
        self._min_reference_threshold = min_reference_threshold
        
        self._dict_thresholds = dict()
        self.calulate_min_threshold()
        self.calulate_max_threshold()
        self.define_eligible_features()
        
        
    @property
    def min_threshold(self) -> pd.Series:
        return self._min_threshold
    
    @property
    def max_threshold(self) -> pd.Series:
        return self._max_threshold
    
    @property
    def eligible_features(self) -> dict:
        return self._eligible_features
    
    @property
    def dict_thresholds(self) -> dict:
        return self._dict_thresholds
        
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
        self._min_threshold = pd.concat(list_thresholds, axis=1).max(axis=1)

    def calulate_max_threshold(self):
        list_thresholds = []
        if self._percentile is not None:
            list_thresholds.append(PercentileThreshold(self.data, 100.0-self._percentile).calculate_threshold())
        if self._min_nb_samples is not None:
            list_thresholds.append(NSampleThreshold(self.data, self._min_nb_samples).calculate_threshold(ascending=False))
        self._max_threshold = pd.concat(list_thresholds, axis=1).min(axis=1)
        
    def define_eligible_features(self):
        eligible_features = self._max_threshold>=self._min_threshold
        self._eligible_features = list(eligible_features[eligible_features].index)
    
    def generate_thresholds(self): 
        for feature in self._eligible_features:
            min_percentile = self.get_threshold_percentile(self.data[feature], self.min_threshold[feature])
            max_percentile = self.get_threshold_percentile(self.data[feature], self.max_threshold[feature])
            threshold_percentiles = np.arange(min_percentile, max_percentile + self._step_percentile, self._step_percentile)
            thresholds = np.array([np.percentile(self.data[feature], p) for p in threshold_percentiles])
            self._dict_thresholds[feature] = pd.DataFrame()
            self._dict_thresholds[feature]['threshold'] = thresholds
            self._dict_thresholds[feature]['threshold_percentile'] = threshold_percentiles
    
    def is_threshold_validated(self, pvalue: float, hazard_ratio: float):
        validated = False
        if (pvalue<0.05 and hazard_ratio>1.0):
            validated = True
        return validated
    
    def generate_cox_expression(self, feature) -> pd.DataFrame:
        cox = pd.DataFrame()
        cox['feature'] = self.data[feature]
        cox['time'] = self._survival_data.loc[cox.index, self._duration_col]
        cox['event'] = self._survival_data.loc[cox.index, self._event_col]
        return cox[['feature', 'time', 'event']]
    
    def generate_cox_group(self, feature, current_threshold):
        cox = self.generate_cox_expression(feature)
        cox['group'] = 0
        cox.loc[cox['feature']>current_threshold, 'group'] = 1
        return cox[['group', 'time', 'event']]
    
    def calculate_cox_model_for_expression(self, feature):
        cox_expression = self.generate_cox_expression(feature)
        cph = CoxPHFitter()
        cph.fit(cox_expression, duration_col='time', event_col='event', show_progress=False)
        cox_pvalue_expression = cph.summary.p['feature']
        cox_hr_expression = cph.summary['exp(coef)']['feature']
        cox_expression_validated = self.is_threshold_validated(cox_pvalue_expression, cox_hr_expression)
    
    def calculate_cox_model_for_thresholds(self, feature):
        pvalues = []
        hrs = []
        validated = []
        for current_threshold in self.dict_thresholds[feature]['threshold']:
            cox_group = self.generate_cox_group(feature, current_threshold)
            cph = CoxPHFitter()
            cph.fit(cox_group, duration_col='time', event_col='event', show_progress=False)
            cox_pvalue_group = cph.summary.p['group']
            pvalues.append(cox_pvalue_group)
            cox_hr_group = cph.summary['exp(coef)']['group']
            hrs.append(cox_hr_group)
            cox_group_validated = self.is_threshold_validated(cox_pvalue_group, cox_hr_group)
            validated.append(cox_group_validated)
        self._dict_thresholds[feature]['p_value'] = pvalues
        self._dict_thresholds[feature]['hazard_ratio'] = hrs
        self._dict_thresholds[feature]['validated'] = validated
            
    
    def calculate_threshold(self) -> pd.Series:
        adaptive_threshold = pd.Series(index=self.data.columns, dtype=float)
        return adaptive_threshold
        
