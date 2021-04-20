import pandas as pd
import numpy as np
from analysis import threshold

# Generate data

np.random.seed(42)

N = 100
tumoral_samples = ['T{:03d}'.format(i+1) for i in range(N)]
normal_samples = ['N{:03d}'.format(i+1) for i in range(N)]

tumoral = pd.DataFrame(index=tumoral_samples, columns=['G1', 'G2'])
tumoral['G1'] = np.random.normal(5, 2, size=(N, 1))
tumoral['G2'] = np.random.normal(5.5, 2, size=(N, 1))
print('tumoral', tumoral.shape)
print(tumoral.head(3))

normal = pd.DataFrame(index=normal_samples, columns=['G1', 'G2'])
normal['G1'] = np.random.normal(0.9, 0.5, size=(N, 1))
normal['G2'] = np.random.normal(1.1, 0.5, size=(N, 1))

# normal['G1'] = np.random.normal(10, 0.5, size=(N, 1))


print('normal', normal.shape)
print(normal.head(3))

# Calculate thresholds

max_normal = threshold.MaxTreshold(normal).calculate_threshold()

percentile = 15.0
step_percentile = 1.0
nb_samples = 20
noise = 0.3

'''
min_percentile = threshold.PercentileThreshold(tumoral, percentile).calculate_threshold() 
min_sample = threshold.NSampleThreshold(tumoral, nb_samples).calculate_threshold(ascending=True)
noise = threshold.NoiseThreshold(tumoral, 0.3).calculate_threshold()

max_percentile = threshold.PercentileThreshold(tumoral, 100.0-percentile).calculate_threshold() 
max_sample = threshold.NSampleThreshold(tumoral, nb_samples).calculate_threshold(ascending=False)


candidate_min_thresholds = pd.concat([max_normal, min_percentile, min_sample, noise], axis=1)
candidate_min_thresholds.columns = ['max_normal', 'min_percentile', 'min_sample', 'noise']
candidate_min_thresholds['max'] = candidate_min_thresholds.max(axis=1)
print('\ncandidate_min_thresholds')
print(candidate_min_thresholds)

candidate_max_thresholds = pd.concat([max_percentile, max_sample], axis=1)
candidate_max_thresholds.columns = ['max_percentile', 'max_sample']
candidate_max_thresholds['min'] = candidate_max_thresholds.min(axis=1)
print('\ncandidate_max_thresholds')
print(candidate_max_thresholds)
'''

data = tumoral
options = {'percentile': percentile, 'min_nb_samples': nb_samples, 'noise_level': noise, 'min_reference_threshold': max_normal}
adaptive_threshold = threshold.AdaptiveThreshold(data=tumoral, **options)


eligible_features =  adaptive_threshold.define_eligible_features()
print('\neligible_features', eligible_features)
 
adaptive_threshold.generate_thresholds()
print(adaptive_threshold.dict_thresholds)

feature = 'G1'
current_threshold = 3.52485183

up = data[data[feature]>current_threshold][feature]
