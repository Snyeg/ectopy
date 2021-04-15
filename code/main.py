import Verification as vf
import pandas as pd
import FrequencyCalcul as frq_cal

df1File='data.csv'
df2File='genes.csv'
df3File='expgroup.csv'

df1=pd.read_csv(df1File,sep=";")
df2=pd.read_csv(df2File,sep=";")
expgroup=pd.read_excel(df3File,index_col=0)

SelectedTissues=["testis","placenta","embryonic"]

df2SelectedTissues=df2.where(df2.tissue.isin(SelectedTissues))

data = df1.merge(df2SelectedTissues, on='id_gene')

expgroup = expgroup[["tissue_status"]]

'''
+["dfs_months"]+["dfs_censor"]]
'''

expgroup = expgroup.dropna()
data = data.dropna()


cty = vf.DataConsistensy()
data,expgroup = cty.check_sample_id(data,expgroup)
stats = cty.calculate_consistensy_stats(data,expgroup)


df2SelectedTissues=df2.where(df2.tissue.isin(SelectedTissues))

#data=data.iloc[5,0:2]

print(data.head(3))
print(expgroup.head(3))



frq = frq_cal.FrequencyCalcul()
tab_frequency = frq.genes_split(data,expgroup,2)


print("\n\ntab_frequency : \n\n", tab_frequency)


    