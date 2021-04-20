from analysis import threshold
import pandas as pd
from lifelines import CoxPHFitter

data_dir = '../data/'

expgroup = pd.read_csv(data_dir + 'expgroup.csv', sep=';', index_col='id_sample')
data = pd.read_csv(data_dir + 'data.csv', sep=';', index_col='id_sample')

print('Data', data.shape)
print(data.head())

expgroup_normal = expgroup[expgroup['group']=='normal']
expgroup_tumoral = expgroup[expgroup['group']=='tumoral']
normal = data.loc[expgroup_normal.index, :]
tumoral = data.loc[expgroup_tumoral.index, :]


# Adaptive threshold

percentile = 15.0
step_percentile = 1.0
nb_samples = 20
noise = 0.3

max_normal = threshold.MaxTreshold(normal).calculate_threshold()

options = {'percentile': percentile, 'step_percentile': step_percentile, 'min_nb_samples': nb_samples, 'noise_level': noise, 'min_reference_threshold': max_normal}
adaptive_threshold = threshold.AdaptiveThreshold(data=tumoral, survival_data=expgroup_tumoral, duration_col='time', event_col='event', **options)
adaptive_threshold.generate_thresholds()

feature = 'EXO1'
print('\nProcessing feature', feature, ' please wait...')
adaptive_threshold.calculate_cox_model_for_thresholds(feature)
dict_thresholds = adaptive_threshold.dict_thresholds
print('Results of Cox model for', feature, ':')
print(dict_thresholds[feature].head())






