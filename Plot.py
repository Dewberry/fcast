# first, list all files that includes specific starting and ending dates
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil # copying files to another directory
import xarray as xr
import netCDF4
from glob import glob
import dask

# Set the current working directory

current_dir = os.getcwd()

# Print path to make sure it is the correct working directory path

#print(current_dir)

# Use the cleaned data from the current working directory
list = glob(os.path.join(current_dir, "clean_data/*"))

#data = pd.Series(os.path.join(current_dir, "clean_data"))
#for file in glob(os.path.join(current_dir, "clean_data/*")):
    # print(file)

ds1 = xr.open_mfdataset(list)
comid = 22340547

ds2 = ds1.sel(feature_id=comid)['streamflow']

df = ds2.to_dataframe()

#ax = df.plot(figsize=(20,8), title = 'Reanalysis Stream Flow for ComID = 229757')
#ax.set(xlabel = 'Date', ylabel = 'StreamFlow(cms)');

plt.figure()
df.streamflow.plot(style='k--', label='Series')
#plt.legend(); plt.legend(loc='best')
plt.xlabel('Days')
plt.ylabel('stream flow (m3/sec)')
plt.title('The Stream Flow Time Series for ComID 229757')
plt.grid(True)
plt.savefig("comid_22340547.png")
plt.show()

#df.plot(kind='line', x='time', y='Stream Flow', ax=ax)


#Data_frame.streamflow.plot()
#plot.show()