# Assim

According to [NOAA on the NWM](https://water.noaa.gov/about/nwm):

> The Standard Analysis and Assimilation configuration cycles hourly and produces a real-time analysis of the current streamflow and other surface and near-surface hydrologic states across the contiguous United States (CONUS). This configuration is internally cycling, with each subsequent Standard Analysis starting from the previous hour’s run. The exception is the 19Z Standard Analysis cycle which ingests initial conditions from the Extended Analysis below. The Standard Analysis also produces restart files each hour which are used to initialize the short-, medium-, and long-range forecast simulations. Meteorological forcing data are drawn from the MRMS Gauge-adjusted and Radar-only observed precipitation products along with short-range RAP and HRRR, while stream-gauge observations are assimilated from the USGS.

Usage:

```python
Assim(self, fs: gcsfs.core.GCSFileSystem, comid: int, date: str, start_hr: int, offset=0, NWMtype='assim')
```
A representation of an Analysis Assimilation NWM netcdf file on GCS

This is used to get the initial time and streamflow for a forecast being made

Parameters:

 - `fs (gcsfs.core.GCSFileSystem)`: The mounted NWM Google Cloud Storage Bucket using gcsfs.
    This is created like so: `fs = gcsfs.GCSFileSystem(project='national-water-model')`
 - `comid (int)`: The ComID that corresponds to the stream segment of interest.
    The ComID is a common identifier (unique) that allows a user of the NHDPlusV21
    to access the same stream segements across the entire NHDPlus anywhere in the
    country. More information [here.](http://www.horizon-systems.com/NHDPlus/NHDPlusV2_documentation.php#NHDPlusV2%20User%20Guide)
 - `date (str)`: The date of the model output being used. (e.g. '20190802' for Aug 2, 2019)
 - `start_hr (int)`: The starting time (UTC) on for the date specified.
 - `hr (int, optional)`: The hour of the analysis assim of interest (e.g. 0, 1, or 2). Defaults to 0

# Attributes / Methods:
## assim_flow
The streamflow at the analysis assimilation time
## assim_time
The analysis assimilation time
## filepath
The filepath of the netcdf on GCS being utilized
## nfiles
The number of available files for this output (NWM v2 has 3 for analysis_assim)
## offset
The hour of the analysis assim of interest (e.g. 0, 1, or 2). Defaults to 0
