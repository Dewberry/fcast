# FloodCast Transportation Tools
Geospatial tools for the FloodCast project focusing on transportation.

### Contents
##### Notebooks
- basic_profile_creation-Dev - simple topographic profile creation using parallel offset lines created from `parallel_transit_lines-Dev` and the best available topographic (bat) data.
- download_bat - download the bat data stored on AWS S3 locally.
- parallel_transit_lines-Dev - create parallel offset lines from snippets of transportation routes intersecting streamlines.

##### Python Files
- localutils - initial python file associated with the above notebooks. Currently only contains the `download_bat` function.