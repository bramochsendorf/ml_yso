import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS

plt.close('all')

# read data
df = pd.read_table('data/jones_2017_ascii.txt',sep='\s+')

# select only features that will be used in training the model (SpClass, 4.5, 8.0, and 24 micron)
df = df[['SpClass','RAJ2000','DEJ2000', '[4.5]','[8.0]','[24]']]

# replace missing values with NaNs, and drop rows containing any NaNs.
df.replace(999.9999, np.nan, inplace=True)
df = df.dropna(axis=0)

# define interesting colors
df['[4.5-8.0]'] = df['[4.5]'] - df['[8.0]']
df['[8.0-24]'] = df['[8.0]'] - df['[24]']

# read in dust opacity (Gordon et al. 2014) and get WCS header info
hdu = fits.open('/data1/python/ml_jwst/lmc_bembb_beta_0.8_2.5_19apr14_dust_param_exp.final.fits')[1]
w = WCS(hdu.header)

# convert world coordinates to image pixels. if coordinates fall outside of boundary, put coordinate to zero
df['xpix_sigmadust'], df['ypix_sigmadust'] = w.all_world2pix(df['RAJ2000'],df['DEJ2000'], 0)
df['xpix_sigmadust'][df['xpix_sigmadust'] > 583] = 0
df['xpix_sigmadust'][df['xpix_sigmadust'] < 0] = 0
df['ypix_sigmadust'][df['ypix_sigmadust'] > 583] = 0
df['ypix_sigmadust'][df['ypix_sigmadust'] < 0] = 0

# Find N_h and CO at each pixel value
df['sigmadust'] = hdu.data[np.int_(np.round(df['ypix_sigmadust'])),np.int_(np.round(df['xpix_sigmadust']))] # convert to surface density

# PLOT ROUTINES
# now plot sigma dust ditributions for each; this shows that YSOs and HII regions have significant higher dust columns. this can be used in classification 
df2 = df.groupby('SpClass')['sigmadust'].mean()
df2.plot(kind='bar',legend=False)
plt.title(r'Log $\Sigma_\mathrm{dust}$ at source')
plt.savefig('output/dust_column_traindata.pdf', dpi=150, bbox_inches='tight', pad_inches=0.2)

# now replace missing dust values with a very small (log) value, because a missing value means below detection threshold.
df['sigmadust'].replace(np.nan,-4, inplace=True)

# save the data?
df.to_pickle('output/features_svm')