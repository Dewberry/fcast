# MediumRange

According to [NOAA on the NWM:](https://water.noaa.gov/about/nwm)

>The Medium Range Forecast configuration is executed four times per day, forced with GFS model output. Member 1 extends out to 10 days while members 2-7 extend out to 8.5 days. This configuration produces 3-hourly deterministic output and is initialized with the restart file from the Analysis and Assimilation configuration.

Usage:

```python
MediumRange(self, fs: gcsfs.core.GCSFileSystem, comid: int, date: str, start_hr: int, members: list = [1, 2, 3, 4, 5, 6, 7], NWMtype='medium')
```
A representation of a Medium Range forecast made using NWM netcdf files on GCS

Pulls the relevant files from GCS to make an 8.5 day streamflow forecast beginning
at a specified date and start time (UTC), with data points in 3 hour steps.

Parameters:

 - `fs (gcsfs.core.GCSFileSystem)`: The mounted NWM Google Cloud Storage Bucket using gcsfs.
    This is created like so: `fs = gcsfs.GCSFileSystem(project='national-water-model')`
 - `comid (int)`: The ComID that corresponds to the stream segment of interest.
    The ComID is a common identifier (unique) that allows a user of the NHDPlusV21
    to access the same stream segements across the entire NHDPlus anywhere in the
    country. More information [here.](http://www.horizon-systems.com/NHDPlus/NHDPlusV2_documentation.php#NHDPlusV2%20User%20Guide)
 - `date (str)`: The date of the model output being used. (e.g. '20190802' for Aug 2, 2019)
 - `start_hr (int)`: The starting time (UTC) on for the date specified.
 - `members (list)`: The members you want the medium range forecast for. Defaults to `[1, 2, 3, 4, 5, 6, 7]`

# Attributes / Methods:

## filepaths
A list of lists, each containing the filepaths used for each member
## forecast_hours
A list of forecast hours. For MediumRange this is hours 3-204 in steps of 3
## mem_dsets
A list of stacked xarray datasets, each representing a member
## members
The members that a MediumRange forecast will be created for
## nfiles
The total number of files used to build the forecast
## get_streamflow
```python
MediumRange.get_streamflow(self, assim_time: str, assim_flow: float) -> pandas.core.frame.DataFrame
```
Get the forecasted streamflow for all selected members in one pandas dataframe, given an assim_time and assim_flow produced using the Assim class.