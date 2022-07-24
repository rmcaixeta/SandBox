from scipy.interpolate import griddata
import numpy as np
import ezdxf
import matplotlib.pyplot as plt
import pandas as pd

# to get proportion of block above/below a not so complex mesh
 
# read dxf or str and get unique pts
doc = ezdxf.readfile('FOLDS2.dxf')
msp = doc.modelspace()

x,y,z = ([],[],[])

for e in msp:
	for v in e.wcs_vertices():
		x.append(v.x)
		y.append(v.y)
		z.append(v.z)

# if surface built from lines, might need to increase point density to work well
c = pd.DataFrame({'X':x,'Y':y,'Z':z}).drop_duplicates()

# get elevation data for each xy; discretization set in dx
dx = 4
bxy = 5
lvl = 4
minx,maxx = [bxy*np.min(c.X)//bxy,bxy+bxy*np.max(c.X)//bxy]
miny,maxy = [bxy*np.min(c.Y)//bxy,bxy+bxy*np.max(c.Y)//bxy]
xi,yi = [np.arange(minx,maxx,bxy/dx), np.arange(miny,maxy,bxy/dx)]
xi,yi = np.meshgrid(xi,yi)
zi = griddata((c.X,c.Y),c.Z,(xi,yi),method='linear')

out = pd.DataFrame({'XI':xi.flatten(),'YI':yi.flatten(),'ZI':zi.flatten()}).dropna().reset_index(drop=True)
out['XB'] = bxy*(out['XI']//bxy)+bxy/2
out['YB'] = bxy*(out['YI']//bxy)+bxy/2
out['ZB'] = lvl*(out['ZI']//lvl)+lvl/2
for c in ['X','Y','Z']: out[c+'B'] = out[c+'B'].round(4)

out['SH'] = out.groupby(['XB','YB'])['ZI'].transform('count')
out['ST'] = out.groupby(['XB','YB','ZB'])['ZI'].transform('count')

out['IN'] = (out['ZI']-(out['ZB']-lvl/2))/lvl
out['IN'] /= out['SH']

# deal with multiple levels inside same XY
# if all other subblocks are in level below, no correction needed
# if some subblock is in level above, need to correct

for idx in out[out['SH']!=out['ST']].index:
	xb = out.loc[idx,'XB']
	yb = out.loc[idx,'YB']
	zb = out.loc[idx,'ZB']
	sh = out.loc[idx,'SH']
	st = out.loc[idx,'ST']
	zo = out.loc[(out['XB']==xb) & (out['YB']==yb),'ZB']
	out.loc[idx,'IN'] += (sum(zo > zb)/(sh*st))


out.rename(columns={'XB':'X','YB':'Y','ZB':'Z','IN':'enplace'},inplace=True)
out = out[['X','Y','Z','enplace']].groupby(['X','Y','Z']).sum().reset_index()
print(out.describe())



# view results
plt.scatter(out['X'],out['Y'],c=out['Z'], cmap='jet')
#plt.imshow(zi, cmap='jet', interpolation='nearest')
plt.colorbar()
plt.show()


