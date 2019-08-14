# get_USGS_stations
```python
get_USGS_stations(comid: int, s3path='s3://nwm-datasets/Data/Vector/USGS_NHDPlusv2/STATID_COMID_dict.json') -> list
```
Given a comid, go find the corresponding USGS gage ids. Currently only works with access to `s3://nwm-datasets/Data/Vector/USGS_NHDPlusv2/STATID_COMID_dict.json`. This functions source code can be easily refactored to accept a comidDict, which can be created by doing the following: 
```python
gdb = 'NHDPlusV21_National_Seamless_Flattened_Lower48.gdb'
src = fiona.open(gdb, layer='NHDFlowline_Network')
comidDict = {src[f]['properties']['COMID']: k for k in src.keys()}
```