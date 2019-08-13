# GageUSGS
```python
GageUSGS(self, gage: str, get_rc: bool = True)
```
USGS stream gage class containing data scraped from USGS websites.

The class currently supports scraping of stream gage metadata
(i.e. vertical datum, lat/lon, etc.), currently available data
at a gage, as well as rating curves and their metadata.

Parameters:

 - `gage (str)`: A string representing a USGS gage id (e.g. '01400000').
 - `get_rc (bool, optional)`: Get the rating curve for the USGS gage. Defaults to True.

## available_data
The data available from the metadata url
## drainage_area_sqmi
Drainage area upstream of the gage in sq miles
## feet_above_vertical_datum
Feet aboe the vertical datum, for stage to elevation conversions
## gage
Gage id string
## horizontal_datum
Horizontal Datum of the gage
## HUC8
HUC8 that the gage is within
## lat
Latitude of the gage
## lon
Longitude of the gage
## metadata
Dictionary of general gage metadata
## metadata_url
Url that the gage metadata is gathered from
## rating_curve
USGS Rating curve at gage location
## rating_curve_metadata
USGS Rating curve metadata at gage location
## vertical_datum
Vertical datum of the gage