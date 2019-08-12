# Resources
#### [Information on the National Water Model](https://water.noaa.gov/about/nwm)
 - The National Water Model outputs are being pulled from [Google Cloud Storage](https://console.cloud.google.com/marketplace/details/noaa-public/national-water-model?filter=category:climate&id=2b3b4e1c-20ad-455c-89c5-7c09b82c7f98) using [gcsfs](https://gcsfs.readthedocs.io/en/latest/).
 
#### [Information on the NDHPlusV21](http://www.horizon-systems.com/NHDPlus/NHDPlusV2_home.php)
- The `NHDPlusV21_National_Seamless_Flattened_Lower48.gdb` is being used. [Dataset and documentation availble for download here](http://www.horizon-systems.com/NHDPlus/V2NationalData.php)

#### [Information on USGS Stream Gages](https://waterdata.usgs.gov/nwis/rt)
- Information for USGS stream gages are being webscraped from an assortment of USGS sites.

---
# Contents

### Notebooks:
 - [__MediumRangeForecasts__](MediumRangeForecasts.ipynb): Retrieve the medium range forecast of streamflow from the outputs of the National Water Model. More information can be found [here under Forecast Configurations.](https://water.noaa.gov/about/nwm)
 - [__NWM_classes-Dev__](NWM_classes-Dev.ipynb): Development space for NWM class objects.
 - [__ShortRangeForecasts__](ShortRangeForecasts.ipynb): Retrieve the short range forecast of streamflow from the outputs of the National Water Model. More information can be found [here under Forecast Configurations.](https://water.noaa.gov/about/nwm)
 - [__USGS_Gages__](USGS_Gages.ipynb): Example usage of the GageUSGS class.
 - [__clean_GageLoc_shp__](clean_GageLoc_shp.ipynb): The notebook used to clean and add attributes to the GageLoc shapefile. The output shapefile/json is used to easily match ComIDs with USGS gage IDs.
 - [__compare_rc_NWM_USGS-Dev__](compare_rc_NWM_USGS-Dev.ipynb): Development space for comparing rating curves from the National Water Model to the rating curves from the USGS.
 - [__explore_NHDPlus-Dev__](explore_NHDPlus-Dev.ipynb): Development space for the StreamSegmentNHD class.
 
*__All of the above notebooks implement code stored in the `fcast` subdirectory__*