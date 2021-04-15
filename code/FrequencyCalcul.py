import pandas as pd

class FrequencyCalcul:
      
    def genes_split (self, data, expgroup, nb_std):
        expgroup_tumoral_index = list(expgroup.index[expgroup["tissue_status"]=="tumoral"])
        expgroup_normal_index = list(expgroup.index[expgroup["tissue_status"]=="normal"])
        
        expgroup_normal = expgroup.drop(expgroup.index[expgroup.index.isin(expgroup_tumoral_index)])
        expgroup_tumoral = expgroup.drop(expgroup.index[expgroup.index.isin(expgroup_normal_index)])

        #normal_samples = list(set(expgroup_normal.tissue).intersection(set(data.columns.tolist())))
        #tumoral_samples = list(set(expgroup_tumoral.tissue).intersection(set(data.columns.tolist())))
        
        normal_samples = list(set(expgroup_normal.index).intersection(set(data.columns.tolist())))
        tumoral_samples = list(set(expgroup_tumoral.index).intersection(set(data.columns.tolist())))

        data_normal = data[normal_samples]
        data_tumoral = data[tumoral_samples]
        print(list(set(expgroup_normal.index)))
        print(data_normal.isnull().sum().sum())
        tab_frequency=FrequencyCalcul.expression_frequency(data,data_normal,data_tumoral,nb_std)
        
        return tab_frequency
    
    def expression_frequency (data, data_normal, data_tumoral, nb_std):
        d={"gene_symbol":[],"treshold":[],"treshold_name":[],"frequency":[],"nb_exprimé":[]}
        tab_frequency = pd.DataFrame(data=d)
        
        
   
        data_normal["mean"] = data_normal.sum(axis=1)
        data_normal["std"] = data_normal.std(axis=1)
        
        print(data_normal["mean"])
        print(data_normal["mean"].isnull().sum().sum())

        idx=0
        for index,row in data_normal.iterrows():
            treshold = row["mean"] + nb_std * row["std"]
            
            data_over_treshold = list(data_tumoral.iloc[idx])
            nb_total_values=len(data_over_treshold)

            for value in data_over_treshold[:]:
                if value < treshold:
                    data_over_treshold.remove(value)
                    
            expression_frequency = len(data_over_treshold)/nb_total_values*100
            new_row={"gene_symbol" : data.index[idx],
                     "treshold" : treshold,
                     "treshold_name" : "m"+str(nb_std)+"sd",
                     "frequency" : expression_frequency,
                     "nb_exprimé" : len(data_over_treshold)
                     }
            tab_frequency=tab_frequency.append(new_row,ignore_index=True)
            idx+=1
        return tab_frequency
'''
expgroup_d = {'tissue': ["1", "2","3", "4","5", "6","7", "8"], 'tissue_status': ["tumoral","tumoral","normal","normal","tumoral","tumoral","normal","normal"]}
data_d = {'gene_symbol': ["AFD", "IOJK", "ABBJK", "IERK"], '1': [0.123,0,0.2,1.23123],'2': [0.36,342,8,2.786],'3': [0,0.0345,2.324,0.432],'4': [0.32,34.342,3.242,23.4234], '5': [0.2,0.3452,0.213,3],'6': [6.36,342,1.3234,2.786],'7': [0.3434,0.0345,0.4,0.432],'8': [0.32,1.342,0.2322,0.4234]}
expgroup = pd.DataFrame(data=expgroup_d)
data = pd.DataFrame(data=data_d)



print("\n\ndata : \n\n", data)
print("\n\nexpgroup : \n\n", expgroup)

tab_frequency = FrequencyCalcul.genes_split(data,expgroup,2)

print("\n\ntab_frequency : \n\n", tab_frequency)
'''