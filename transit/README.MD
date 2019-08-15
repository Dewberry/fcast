# FloodCast Transportation Tools
Geospatial tools for the FloodCast project focusing on transportation.

### Contents
##### Notebooks
- advanced_profile_creation-Dev - code development focused on creating topographic profiles from transportation routes and a digital elevation model. Additional tasks include: 1) filtering road points to reverse hydro-enforcement; 2) plotting code to review transportation routes in map-view; 3) identification of the nearest point along the transportation route to the channel minimum.
- delta_class-Dev - development notebook for the `DepthToInundationPts` class object now found in `TransitOps.py`. Retained as a showcase notebook.
- dense_profile_creation-Dev - copy of the main portion of `advanced_profile_creation-Dev` with the additional capability of densifiying verticies along the offset and transportation lines.
- download_bat - download the bat data stored on AWS S3 locally.

##### Python Files
- localutils - initial python file associated with the above notebooks. Currently only contains the `download_bat` function.
- TransitOps - contains the `DepthToInundationPts` class object along with helper functions.