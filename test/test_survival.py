from analysis import survival
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


# survival_model = survival.Cox(survival_data=expgroup_tumoral, duration_col='time', event_col='event')
survival_model = survival.Logrank(survival_data=expgroup_tumoral, duration_col='time', event_col='event')

model_output = survival_model.calculate_model_for_threshold('EXO1', 2.126367, tumoral)
significant = survival_model.is_significant(model_output)
print('p-value, hr', model_output, 'significant', significant)

