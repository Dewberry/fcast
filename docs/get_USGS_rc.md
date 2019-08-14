# get_USGS_rc
```python
get_USGS_rc(comid: int)
```
Given a comid, get the rating curve for the matching USGS Gages. currently only works with access to `s3://nwm-datasets/Data/Vector/USGS_NHDPlusv2/STATID_COMID_dict.json`.