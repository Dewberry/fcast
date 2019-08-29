# reanalysis
An initial look at the NWM reanalysis netcdf files.

 - [__Clean_data_By_date__](reanalysis/Clean_data_By_date.py): Organizing downloaded data by dates.
 - [__Download_Reanalysis_Data__](reanalysis/Download_Reanalysis_Data.py): Downloading reanalysis netcdf files from s3.
 - [__Plot__](reanalysis/Plot.py): Plotting NWM reanalysis data.
 - [__Time_series__](reanalysis/Time_Series.py): Making a time series at a specific ComID.
 - [__explore_reanalysis-Dev__](reanalysis/explore_reanalysis-Dev.ipynb): A notebook for downloading a time series of reanalysis data from s3 and making a streamflow time series plot at one ComID.
 - [__reanalysis__](reanalysis/reanalysis.py): Functions used in the __explore_reanalysis-Dev__ notebook.