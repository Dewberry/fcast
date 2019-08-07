# FloodCast Transportation Tools
Geospatial tools for the FloodCast project focusing on transportation.

### Contents
##### Notebooks
- advanced_profile_creation-Dev - code development focused on creating topographic profiles from transportation routes and a digital elevation model. Further analysis is carried out on filtering these profiles to more accurately determine channel minima to transportation route different (i.e. $\Delta$Z).
- download_bat - download the bat data stored on AWS S3 locally.

##### Python Files
- localutils - initial python file associated with the above notebooks. Currently only contains the `download_bat` function.