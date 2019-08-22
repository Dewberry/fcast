


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

print(current_dir)

# Use the cleaned data from the current working directory
list = glob(os.path.join(current_dir, "clean_data/*"))

#data = pd.Series(os.path.join(current_dir, "clean_data"))
#for file in glob(os.path.join(current_dir, "clean_data/*")):
    # print(file)

ds1 = xr.open_mfdataset(list[0:100])
comid = 229757
ds2 = ds1.sel(feature_id=comid)['streamflow']

Data_frame = ds2.to_dataframe()


#Data_frame.streamflow.plot()
#plot.show()