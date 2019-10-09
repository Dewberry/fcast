<img src="docs/img/main_graphic.png" alt="fcast" width=100% height=auto>

# [fcast](https://dewberry.github.io/fcast/)

---

## Description
__fcast__ is a collection of python tools used for forecasting flood events and their impact on transportation infrastructure. The following datasets are used:
- [The NHDPlus V2.1 dataset](http://www.horizon-systems.com/NHDPlus/NHDPlusV2_home.php)
- Staged Elevation from [The National Map](https://www.usgs.gov/core-science-systems/national-geospatial-program/national-map). 
  - [FTP LINK](ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/)
- [USGS National Transportation Dataset (NTD)](https://catalog.data.gov/dataset/usgs-national-transportation-dataset-ntd-downloadable-data-collectionde7d2)
- [The National Water Model (NWM)](https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model?filter=category:climate&id=2b3b4e1c-20ad-455c-89c5-7c09b82c7f98)
  - [More information](https://water.noaa.gov/about/nwm)
  
---

## Installation

See https://dewberry.github.io/fcast/setup/ for installation details.

---
  
## Contents
`fcast` - The collection of core .py files.
 - [__GageUSGS__](fcast/GageUSGS.py): An API for webscraping stream gage data from various USGS websites.
 - [__NHDPlusStreamSegment__](fcast/NHDPlusStreamSegment.py): An API for quick and easy access to the NHDPlus V2.1.
 - [__NWM__](fcast/NWM.py): An API for quick and easy access to the [NWM output files](https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model?filter=category:climate&id=2b3b4e1c-20ad-455c-89c5-7c09b82c7f98).
 - [__plotting__](fcast/plotting.py): Functions for plotting using matplotlib and pandas.
 
`notebooks` - The collection of [Jupyter Notebooks](https://jupyter.org/) running the code in the fcast subdirectory. Jupyter Notebooks are used because they produce easy, reproducible, and accesible outputs.
 - [__MediumRangeForecasts__](notebooks/MediumRangeForecasts.ipynb): Retrieve the medium range forecast of streamflow from the outputs of the National Water Model. More information can be found [here under Forecast Configurations.](https://water.noaa.gov/about/nwm)
 - [__NWM_classes-Dev__](notebooks/NWM_classes-Dev.ipynb): Development space for NWM class objects.
 - [__ShortRangeForecasts__](notebooks/ShortRangeForecasts.ipynb): Retrieve the short range forecast of streamflow from the outputs of the National Water Model. More information can be found [here under Forecast Configurations.](https://water.noaa.gov/about/nwm)
 - [__USGS_Gages__](notebooks/USGS_Gages.ipynb): Example usage of the GageUSGS class.
 - [__clean_GageLoc_shp__](notebooks/clean_GageLoc_shp.ipynb): The notebook used to clean and add attributes to the GageLoc shapefile. The output shapefile/json is used to easily match ComIDs with USGS gage IDs.
 - [__compare_rc_NWM_USGS-Dev__](notebooks/compare_rc_NWM_USGS-Dev.ipynb): Development space for comparing rating curves from the National Water Model to the rating curves from the USGS.
 - [__explore_NHDPlus-Dev__](notebooks/explore_NHDPlus-Dev.ipynb): Development space for the StreamSegmentNHD class.
 
`notebooks/data_exploration` - A collection of Jupyter notebooks used for exploring 1D and 2D NWM rating curves and retrieving NWM HAND datasets.
 - [__rating_curves__](notebooks/data_exploration/rating_curves.ipynb): Exploration and comparison of the `hydroprop-fulltable-HUC6.nohand0.csv` and `hydroprop-fulltable-HUC6.csv` rating curve files.
 - [__rating_curves_1D_nc__](notebooks/data_exploration/rating_curves_1D_nc.ipynb): Exploration of rating curves from the NWM 1D netcdf file.
 - [__rating_curves_2D_nc__](notebooks/data_exploration/rating_curves_2D_nc.ipynb): Exploration of rating curves from the NWM 2D netcdf file.
 - [__retrieve_HAND_datasets__](notebooks/data_exploration/retrieve_HAND_datasets.ipynb): Download of HAND datasets for data exploration.
 
`reanalysis` - An initial look at the NWM reanalysis netcdf files.
 - [__Clean_data_By_date__](reanalysis/Clean_data_By_date.py): Organizing downloaded data by dates.
 - [__Download_Reanalysis_Data__](reanalysis/Download_Reanalysis_Data.py): Downloading reanalysis netcdf files from s3.
 - [__Plot__](reanalysis/Plot.py): Plotting NWM reanalysis data.
 - [__Time_series__](reanalysis/Time_Series.py): Making a time series at a specific ComID.
 - [__explore_reanalysis-Dev__](reanalysis/explore_reanalysis-Dev.ipynb): A notebook for downloading a time series of reanalysis data from s3 and making a streamflow time series plot at one ComID.
 - [__reanalysis__](reanalysis/reanalysis.py): Functions used in the __explore_reanalysis-Dev__ notebook.
 
## [View the Documentation](https://dewberry.github.io/fcast/)
