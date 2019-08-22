# This script is used to clean data by date from the downloaded data from the NOAA Reanalysis NWM
# The downloaded data is in a directory called output
# before running this script "clean_data" directory needs to be created


# Used libraries

import pandas as pd
import os
import shutil # copying files to another directory
import xarray as xr
import netCDF4
# Use the current directory as the script. This is used to avoid having hard coded paths.

file_path = os.getcwd()

# The list of files will be in the the output directory

files = pd.Series(os.listdir(file_path + "/output/"))

# first, list all files that includes specific starting and ending dates
# second, iterate over dates and copy the data to the clean_data directory.

for date in pd.date_range('2003-09-10', '2003-10-10', freq="1H").strftime('%Y%m%d'):
    # print(date)
    for file_name in files[files.str.contains(date)]:
        shutil.copy(file_path + "output/" + file_name, file_path + '/clean_data/')
