from service.data_consistency import DataConsistency
from analysis import threshold, expression_analysis
import pandas as pd

data_dir = '../data/'
expgroup = pd.read_csv(data_dir + 'expgroup.csv', sep=';', index_col='id_sample')
data = pd.read_csv(data_dir + 'data.csv', sep=';', index_col='id_sample')

print('Data', data.shape)
print(data.head())

consistency = DataConsistency().calculate_consistency_stats(data, expgroup)
print('\nConsistency check')
print(consistency)

expgroup_normal = expgroup[expgroup['group']=='normal']
expgroup_tumoral = expgroup[expgroup['group']=='tumoral']
normal = data.loc[expgroup_normal.index, :]
tumoral = data.loc[expgroup_tumoral.index, :]

mean_threshold = threshold.MeanThreshold().calculate_threshold(normal)
print('\nmean threshold')
print(mean_threshold)

m2sd_threshold = threshold.MeanNStdThreshold().calculate_threshold(normal, n_std=2)
print('\nm2sd threshold')
print(m2sd_threshold)

frequency = expression_analysis.ExpressionFrequency().calculate_expression_frequency(tumoral, m2sd_threshold)
print('\nActivation frequency obtained with m2sd threshold in percentage')
print(frequency.head())



