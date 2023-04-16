
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

infile1 = 'abc.csv'
infile2 = 'def.csv'

cols = ['Cat domain','pct_Fe2O3','pct_SiO2','pct_Ni','pct_MgO']
df = [pd.read_csv(infile1,low_memory=False,usecols=cols,na_values=-1).dropna()]
df += [pd.read_csv(infile2,low_memory=False,usecols=cols,na_values=-1).dropna()]
df = pd.concat(df)

x = ['pct_Fe2O3','pct_SiO2','pct_Ni','pct_MgO']
std = StandardScaler().fit_transform(df[x].values)
neigh = KNeighborsClassifier(n_neighbors=10)
neigh.fit(std, df['Cat domain'])
proba = neigh.predict_proba(std)
df['est'] = neigh.predict(std)

for i,d in enumerate(neigh.classes_):
	df['prob_'+d] = [x[i] for x in proba]

df.to_csv('check_probs.csv',index=False)
