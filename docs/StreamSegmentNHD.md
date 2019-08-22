# StreamSegmentNHD

StreamSegmentNHD is a class object that represents a stream segment
in the NHDPlusV2.1. It is built for easy access to a single stream
segment represented by a ComID without overburdening memory. It is
meant for the NHDPlusV21_National_Seamless_Flattened_Lower48.gdb. It
also requires a ComID dictionary used as a map, which can be found at
`s3://nwm-datasets/Data/Vector/NHDPlusV21_CONUS_seamless/comidDict_NHDPlusV21.json`
or can be made using fiona like so:
```python
gdb = 'NHDPlusV21_National_Seamless_Flattened_Lower48.gdb'
src = fiona.open(gdb, layer='NHDFlowline_Network')
comidDict = {src[f]['properties']['COMID']: k for k in src.keys()}
```

```python
StreamSegmentNHD(self, comid: int, comidDict: dict, src: fiona.collection, warning: bool = True)
```
A representation of one individual NHDPlusV2.1 ComID stream segment.

For detailed information on the dataset, download the Release Notes from [here](http://www.horizon-systems.com/NHDPlusData/NHDPlusV21/Data/NationalData/0Release_Notes_NationalData_Seamless_GeoDatabase.pdf)

All property docstrings have been pulled from these release notes.

Parameters:

 - `comid (int)`: The comID that corresponds to the stream segment of interest.
 - `comidDict (dict)`: The dictionary used to map the ComIDs to the feature index in
                  the gdb. Generally loaded into memory using json.load(filepath)
 - `src (fiona.collection)`: The open fiona collection representing the gdb and the
                        'NHDFlowline_Network' layer.
 - `warning (bool, optional)`: Defaults to true. Raises a warning to ensure the comidDict
                          NHDPlus version matches that of the gdb.

# Attributes / Methods:
## annual_mean_flow_QA
Mean Annual Flow from runoff (cfs)
## annual_mean_flow_QC
Mean Annual Flow with Reference Gage Regression applied to QB (cfs). Best EROM estimate of "natural" mean flow.
## annual_mean_flow_QE
Mean Annual Flow from gage adjustment (cfs). Best EROM estimate of actual mean flow.
## annual_mean_vel_QA
Mean Annual Velocity for QA (fps)
## annual_mean_vel_QC
Mean Annual Velocity for QC (fps). Best EROM estimate of "natural" mean velocity.
## annual_mean_vel_QE
Mean Annual Velocity from gage adjustment (fps). Best EROM estimate of actual mean velocity.
## attrs
An OrderedDict of all attributes for the stream segment
## comid
Common identifier of the NHD feature
## comidDict
Dictionary containing the ComID -> feature index map
## crs_proj4
The crs of the dataset as a proj4 string
## crs_wkt
The crs of the dataset as wkt
## current_month_QV

    'QA': 'Mean Annual Flow from runoff (cfs)',
    'VA': 'Mean Annual Velocity for QA (fps)',
    'QC': 'Mean Annual Flow with Reference Gage Regression applied to QB (cfs). 
           Best EROM estimate of "natural" mean flow.',
    'VC': 'Mean Annual Velocity for QC (fps). Best EROM estimate of "natural" mean velocity.',
    'QE': 'Mean Annual Flow from gage adjustment (cfs). Best EROM estimate of actual mean flow.',
    'VE': 'Mean Annual Velocity from gage adjustment (fps). Best EROM estimate of actual mean velocity.

## feat_currency_date
Feature Currency Date
## from_node_id
Unique identifier for the point at the top of the NHDFlowline feature
## geometry
Shapely representation of the line segment
## GNIS_id
Geographic Names Information System ID for the value in GNIS_Name
## GNIS_name
Feature Name from the Geographic Names Information System
## length_km
Feature length in kilometers
## max_elev_raw
Maximum elevation (unsmoothed) in centimeters
## max_elev_smoothed
Maximum elevation (smoothed) in centimeters
## min_elev_raw
Minimum elevation (unsmoothed) in centimeters
## min_elev_smoothed
Minimum elevation (smoothed) in centimeters
## QV_meta
Metadata describing the results of current_month_QV
## reach_code
Reach Code assigned to feature
## resolution
NHD database resolution (i.e. 'high', 'medium' or 'local')
## src
The opened fiona collection of the gdb and the 'NHDFlowline_Network' layer
## stream_order
Modified Strahler Stream Order
## tidal
Is Flowline Tidal? 1=yes, 0=no
## to_node_id
Unique identifier for the point at the end of the NHDFlowline feature
## tot_drainage_area_sqkm
Total upstream catchment area from downstream end of flowline.
## WB_area_comid
ComID of the NHD polygonal water feature through which a NHD "Artificial Path" flowline flows