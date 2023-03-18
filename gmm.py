# import libraries (some are for cosmetics)
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from sklearn.mixture import GaussianMixture as GMM
import pandas as pd

n_optimal = 2
elem = 'pct_Fe2O3'

#plt.axvline(60)
#plt.axvline(35)

df = pd.read_csv(na_values=-1)

x = df[[elem]].dropna().values

# create GMM model object
gmm = GMM(n_components = n_optimal, max_iter=1000, random_state=10, covariance_type = 'full').fit(x)

# find useful parameters
mean = gmm.fit(x).means_  
covs  = gmm.fit(x).covariances_
weights = gmm.fit(x).weights_

# create necessary things to plot
x_axis = np.linspace(df[elem].min(), df[elem].max(), 100)

# Plot 2
plt.hist(x, density=True, color='black', bins=50)

sumy = []
for i in range(n_optimal):
	y_axis_i = norm.pdf(x_axis, float(mean[i][0]), np.sqrt(float(covs[i][0][0])))*weights[i]
	plt.plot(x_axis, y_axis_i, lw=3, c='C0')
	sumy.append(y_axis_i)

plt.plot(x_axis, sum(sumy), lw=3, c='C2', ls='dashed')

plt.xlabel(elem)
plt.ylabel("Density")

plt.tight_layout()
plt.show()
plt.close('all')
