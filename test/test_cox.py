from analysis import threshold
import pandas as pd

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

options = {
    'percentile': percentile,
    'step_percentile': step_percentile,
    'min_nb_samples': nb_samples,
    'noise_level': noise,
    'min_reference_threshold': max_normal,
    'nb_folds': 3,
    'nb_cross_validations': 1
    }


adaptive_threshold = threshold.AdaptiveThreshold(data=tumoral, survival_data=expgroup_tumoral, duration_col='time', event_col='event', **options)
adaptive = adaptive_threshold.calculate_threshold()
print(adaptive)
print(adaptive_threshold.get_details('EXO1'))
    
