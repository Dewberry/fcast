# fcast

---

# Description
__fcast__ is a collection of python tools used for forecasting flood events and their impact on transportation infrastructure. the following datasets are used:
- [The NHDPlus V2.1 dataset](http://www.horizon-systems.com/NHDPlus/NHDPlusV2_home.php)
- Staged Elevation from [The National Map](https://www.usgs.gov/core-science-systems/national-geospatial-program/national-map). 
  - [FTP LINK](ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/)
- [USGS National Transportation Dataset (NTD)](https://catalog.data.gov/dataset/usgs-national-transportation-dataset-ntd-downloadable-data-collectionde7d2)
- [The National Water Model](https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model?filter=category:climate&id=2b3b4e1c-20ad-455c-89c5-7c09b82c7f98)
  - [More information](https://water.noaa.gov/about/nwm)
  
---
  
# Contents
`fcast` - The collection of core .py files.
 - [__GageUSGS__](fcast/GageUSGS.py): An API for webscraping stream gage data from various USGS websites.
 - [__NHDPlusStreamSegment__](fcast/NHDPlusStreamSegment.py): An API for quick and easy access to the NHDPlus V2.1.
 - [__NWM__](fcast/NWM.py): An API for quick and easy access to the [NWM output files](https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model?filter=category:climate&id=2b3b4e1c-20ad-455c-89c5-7c09b82c7f98).
 - [__plotting__](fcast/plotting.py): Functions for plotting using matplotlib and pandas.
 
`notebooks` - The collection of [jupyter notebooks](https://jupyter.org/) running the code found in fcast for easy, reproducible, and accesible outputs
 - [__MediumRangeForecasts__](notebooks/MediumRangeForecasts.ipynb): Retrieve the medium range forecast of streamflow from the outputs of the National Water Model. More information can be found [here under Forecast Configurations.](https://water.noaa.gov/about/nwm)
 - [__NWM_classes-Dev__](notebooks/NWM_classes-Dev.ipynb): Development space for NWM class objects.
 - [__ShortRangeForecasts__](notebooks/ShortRangeForecasts.ipynb): Retrieve the short range forecast of streamflow from the outputs of the National Water Model. More information can be found [here under Forecast Configurations.](https://water.noaa.gov/about/nwm)
 - [__USGS_Gages__](notebooks/USGS_Gages.ipynb): Example usage of the GageUSGS class.
 - [__clean_GageLoc_shp__](notebooks/clean_GageLoc_shp.ipynb): The notebook used to clean and add attributes to the GageLoc shapefile. The output shapefile/json is used to easily match ComIDs with USGS gage IDs.
 - [__compare_rc_NWM_USGS-Dev__](notebooks/compare_rc_NWM_USGS-Dev.ipynb): Development space for comparing rating curves from the National Water Model to the rating curves from the USGS.
 - [__explore_NHDPlus-Dev__](notebooks/explore_NHDPlus-Dev.ipynb): Development space for the StreamSegmentNHD class.
 
`docs` - In development.