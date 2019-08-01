# Various functions to be deployed on local machines
#
# Authors:
#      John Wall (jwall@Dewberry.com)
#      Alec Brazeau (abrazeau@dewberry.com)
#
# Copyright: Dewberry Engineers, Inc.
#
# Notes: Modification of Brazeau's wselutils.py file.
#
# ----------------------------------------------------------------------

# Standard/Utility libs
import os

# Geospatial libraries
import geopandas as gpd


def download_bat(reference_grid:gpd.geodataframe.GeoDataFrame, aoi_poly:gpd.geoseries.GeoSeries, output_location:str):
    ''' Download the Best Available Topographic data which covers one or
        more areas of interest.
    '''
    tiffs = []
    for poly in aoi_poly:
        intersecting_tiffs = reference_grid[reference_grid.geometry.apply(lambda row: poly.intersects(row))].tif_name
        tiffs = tiffs + list(intersecting_tiffs)
    
    unique_tiffs = list(set(tiffs))
        
    for tiff in unique_tiffs:
        print('/'.join([output_location, tiff.split('/')[-1]]))
        os.system("aws s3 cp {} {}".format(tiff, output_location))