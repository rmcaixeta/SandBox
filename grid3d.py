from scipy.interpolate import griddata
import numpy as np
import pandas as pd

#read dhs
#read soft pts
dfa = pd.read_csv('raw_data.csv',usecols=['HOLEID','Lamb_X_m','Lamb_Y_m','Z_FROM','Z_TO','Geol_Unit'])
dfa = dfa[dfa['Geol_Unit'].between(0.5,4.5)].reset_index(drop=True)
dfa['SOFT_SAPBED'] = 0

dfa['Lamb_X_m'] = dfa['Lamb_X_m'].round(0).astype(int)
dfa['Lamb_Y_m'] = dfa['Lamb_Y_m'].round(0).astype(int)

cols = ['HOLEID','Lamb_X_m','Lamb_Y_m','Geol_Unit','SOFT_SAPBED']
maxto = dfa[cols+['Z_TO']].groupby(cols).max().reset_index()['Z_TO']
dfa = dfa[cols+['Z_FROM']].groupby(cols).min().reset_index()
dfa['Z_TO'] = maxto
dfa['count'] = dfa.groupby(['HOLEID'])['Geol_Unit'].transform('count')

hd = (dfa['Geol_Unit']==4) & (dfa['count']>1)
hd = dfa[hd]

cols = ['HOLEID','Lamb_X_m','Lamb_Y_m','Z_TO','SOFT_SAPBED']
dfa.loc[~dfa['HOLEID'].isin(hd['HOLEID'].unique()),'SOFT_SAPBED'] = 1
soft = dfa.loc[~dfa['HOLEID'].isin(hd['HOLEID'].unique()),cols]
soft = soft.sort_values('Z_TO').drop_duplicates('HOLEID')



#get z contact sap-bed and cont lat - thick sap
z_soft = griddata((hd['Lamb_X_m'], hd['Lamb_Y_m']), hd['Z_FROM'], (soft['Lamb_X_m'], soft['Lamb_Y_m']))
soft['Z_FROM'] = np.clip(z_soft,-99,soft['Z_TO'])

miss = soft['Z_FROM'].isnull()
z_soft = griddata((hd['Lamb_X_m'], hd['Lamb_Y_m']), hd['Z_FROM'], (soft.loc[miss,'Lamb_X_m'], soft.loc[miss,'Lamb_Y_m']),method='nearest')
soft.loc[miss,'Z_FROM'] = np.clip(z_soft,-99,soft.loc[miss,'Z_TO'])


cols = ['Lamb_X_m','Lamb_Y_m','Z_FROM','SOFT_SAPBED']
out_ = pd.concat([hd[cols],soft[cols]])
out_['Z_FROM'] = out_['Z_FROM'].round(2)
out_.rename(columns={'Z_FROM':'Z_SAPBED'},inplace=True)
out_.to_csv('check.csv',index=False)



#dfa.groupby(['HOLEID','Geol_Unit'])['LENGTH'].transform('sum')
#dfa['LENGTH'] = dfa['Z_TO']-dfa['Z_FROM']
#dfa.groupby(['HOLEID','Geol_Unit'])['LENGTH'].transform('sum')

#calc:
#BED: z, min z, max z
#SAP: thick, min thick, max thick
#EARTHY: thick, min thick, max thick
#ROCKY: thick, min thick, max thick
#FRACT: thick, min thick, max thick
