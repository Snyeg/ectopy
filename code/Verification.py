import numpy as np
class DataConsistensy:
      
    def check_sample_id (self, data, expgroup):
        if 'id_sample' in expgroup.columns:
            expgroup.index = expgroup['id_sample']
            expgroup = expgroup.drop(columns = ['id_sample'])

        data.index = data['gene_symbol']
        data = data.drop(columns=['gene_symbol'])
        
        expgroup=expgroup.dropna()
        data=data.dropna()
        common_samples = list(set(expgroup.index).intersection(set(data.columns)))
        expgroup = expgroup.loc[common_samples,:]
        data = data[common_samples]
        
        return data, expgroup

    def calculate_consistensy_stats(self, data, expgroup):
        stats = dict()
        common_samples = list(set(expgroup.index).intersection(set(data.columns)))
        stats['expgroup'] = dict() 
        stats['data'] = dict() 
        stats['expgroup']['n_samples'] = expgroup.shape[0]
        stats['data']['n_samples'] = data.shape[1]
        stats['n_common_samples'] = len(common_samples)
        stats['common_samples'] = common_samples
        return stats
    

