# Zarr Demo Notebooks 

*created by @sduncan4*

This folder describes the following aspects of zarr arrays and groups:

1. Write a zar file:
    1. Specify bucket
    - Write file
    - Give options
- Read a zar file from a known location
    1. Get attribtues
    - Copy to local
- Search S3 for zarr
    1. Print inventory
    - Look in files
    - Copy a file
    - Etc…

## Create Zarr Files

1. Gather Sources for Creating Zarr Files
- Define where to save and store the zarr file
- Create Zarr Group File
    - Metadata needs to be added to help navigation and tif recreation later
- Write Multiple Datasets to same zarr group
- Write zarrs as Wate Surface Elevations or Booleans

## Read Zarr Files

1. Define and read in zarr group
- From __Create Zarr Files__ we can read the `.attrs.keys()` to see groups inside
- With keys we can search chunk data from each group
- Arrays can be read in with numpy

## Math with Zarr Arrays


