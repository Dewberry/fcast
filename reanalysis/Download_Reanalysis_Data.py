# This script is used to download the reanalysis data from AWS for the CHRTOUT
# https://docs.opendata.aws/nwm-archive/readme.html NOAA National Water Model Reanalysis Model data on AWS documentation
# We are using the CHRTOUT product the stream flow value at points associated with the flow lines for every hour.
# A directory called output needs to be created before running the script.
# The downloaded data will be located in a directory called output.
# The output directory will be in the same level as the script in the current working directory.
# This script can be used to download different products from the Reanalysis data.
# The Reanalysis data products are RTOUT, CHRTOUT, LAKEOUT, and LDASOUT

import boto3
import os
import pathlib as pl
#import io
import dask
import netCDF4
import xarray as xr
import pandas as pd
s3client = boto3.client("s3")
s3 = boto3.resource('s3')
bucket='nwm-archive'
prefix = '2003'
s3Obj = s3.Object(bucket_name=bucket, key=prefix)
print(s3Obj)


# Amazon Ops
def s3List(bucketName, prefixName, nameSelector, fileformat):
    '''
        This function takes an S3 bucket name and prefix (flat directory path) and returns a list of netcdf file.
            This function utilizes boto3's continuation token to iterate over an unlimited number of records.

        BUCKETNAME -- A bucket on S3 containing GeoTiffs of interest
        PREFIXNAME -- A S3 prefix.
        NAMESELECTOR -- A string used for selecting specific files. E.g. 'SC' for SC_R_001.tif.
        FILEFORMAT -- A string variant of a file format.
    '''
    # Set the Boto3 client
    s3_client = boto3.client('s3')
    # Get a list of objects (keys) within a specific bucket and prefix on S3
    keys = s3_client.list_objects_v2(Bucket=bucketName, Prefix=prefixName)
    # Store keys in a list
    keysList = [keys]
    # While the boto3 returned objects contains a value of true for 'IsTruncated'
    while keys['IsTruncated'] is True:
        # Append to the list of keys
        # Note that this is a repeat of the above line with a contuation token
        keys = s3_client.list_objects_v2(Bucket=bucketName, Prefix=prefixName,
                                         ContinuationToken=keys['NextContinuationToken'])
        keysList.append(keys)

    # Create a list of GeoTiffs from the supplied keys
    #     While tif is hardcoded now, this could be easily changed.
    pathsList = []
    for key in keysList:
        paths = ['s3://' + bucketName + '/' + elem['Key'] for elem in key['Contents'] \
                 if elem['Key'].find('{}'.format(nameSelector)) >= 0 and elem['Key'].endswith(fileformat)]
        pathsList = pathsList + paths

    return pathsList


datafiles = s3List(bucket, prefix, 'CHRTOUT', 'DOMAIN1.comp')
#datafile = datafiles[0]
# print(datafiles)


for obj in datafiles:
    filename = obj.split("/")[-1]
    # print(obj)
    s3client.download_file(bucket,prefix+'/'+filename, "./output/" + filename)

