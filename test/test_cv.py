from analysis import cross_validation
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

tumoral = tumoral.iloc[0:10]

targets = pd.Series(index=tumoral.index, dtype=float)
targets.iloc[0:5] = 0.0
targets.iloc[5:10] = 1.0


options = {
    'data': tumoral,
    'nb_folds': 3,
    'nb_cross_validations': 1
    }

strategy = cross_validation.StratifiedKFoldStrategy(**options, targets=targets)
strategy.split()
for cv in  strategy.cross_validations:
    print(cv)

