# Overview

`fcast` is a collection of python tools used for leveraging National Water Model and other data products to forecast flood events and their potential impacts on transportation infrastructure. 


The following datasets are used:

- [The NHDPlus V2.1 dataset](http://www.horizon-systems.com/NHDPlus/NHDPlusV2_home.php)
    - In particular, the _NHDPlusV21_National_Seamless_Flattened_Lower48.gdb_ is utilized.
- Staged Elevation from [The National Map](https://www.usgs.gov/core-science-systems/national-geospatial-program/national-map). 
    - [FTP](ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/)
- [USGS National Transportation Dataset (NTD)](https://catalog.data.gov/dataset/usgs-national-transportation-dataset-ntd-downloadable-data-collectionde7d2)
- [The National Water Model (NWM)](https://water.noaa.gov/about/nwm)
    - [GCS](https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model?filter=category:climate&id=2b3b4e1c-20ad-455c-89c5-7c09b82c7f98)
    - [AWS](https://docs.opendata.aws/noaa-nwm-pds/readme.html)