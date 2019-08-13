# ShortRange
```python
ShortRange(self, fs: gcsfs.core.GCSFileSystem, comid: int, date: str, start_hr: int, NWMtype='short')
```
A representation of a Short Range forecast made using NWM netcdf files on GCS

Pulls the relevant files from GCS to make an 18 hour streamflow forecast beginning
at a specified date and start time (UTC).

Parameters:

 - `fs (gcsfs.core.GCSFileSystem)`: The mounted NWM Google Cloud Storage Bucket using gcsfs.
    This is created like so: `fs = gcsfs.GCSFileSystem(project='national-water-model')`
 - `comid (int)`: The ComID that corresponds to the stream segment of interest.
    The ComID is a common identifier (unique) that allows a user of the NHDPlusV21
    to access the same stream segements across the entire NHDPlus anywhere in the
    country. More information at:
    http://www.horizon-systems.com/NHDPlus/NHDPlusV2_documentation.php#NHDPlusV2%20User%20Guide
 - `date (str)`: The date of the model output being used. (e.g. '20190802' for Aug 2, 2019)
 - `start_hr (int)`: The starting time (UTC) on for the date specified.

## ds
The stacked xarray dataset representing the forecast
## filepaths
A list of the filepaths used to build the forecast
## forecast_hours
A list of forecast hours. For ShortRange this is hours 1-18
## nfiles
The number of files that make up the forecast
## get_streamflow
```python
ShortRange.get_streamflow(self, assim_time: str, assim_flow: float) -> pandas.core.frame.DataFrame
```
Get the streamflow forecast in a pandas dataframe