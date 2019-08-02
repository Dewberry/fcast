
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

# Use the cleaned data from the current working directory
list = glob(os.path.join(current_dir, "clean_data/*"))


ds1 = xr.open_mfdataset(list)
comid = 22340547

ds2 = ds1.sel(feature_id=comid)['streamflow']

df = ds2.to_dataframe()

plt.figure()
df.streamflow.plot(style='k--', label='Series')
#plt.legend(); plt.legend(loc='best') # In case uf you need to add a legend
plt.xlabel('Days')
plt.ylabel('stream flow (m3/sec)')
plt.title('The Stream Flow Time Series for ComID 229757')
plt.grid(True)
plt.savefig("comid_22340547.png")
plt.show()
