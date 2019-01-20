import os, sys, time, glob, bsddb3, s3fs, boto3, math
import psutil
from io import BytesIO
import pathlib as pl
import zarr as zr
#from zarr import blosc
import xarray as xr
import pandas as pd
import numpy as np
from osgeo import gdal, osr
from matplotlib import pyplot as plt
from IPython.display import display, Markdown, Latex

path = str
pl_path = pl.PurePath
ListOfPaths = list([path,path])
zarr_group = zr.group

def mprint(txt:str) -> print:
    '''Print Text as Markdown for Jupyter Lab and Notebooks'''
    display(Markdown(txt))
    
def CreateZarrZipStore(zip_path:path):
    '''Creates a Zip Store for Zarr if saving to local disk.
    Not Applicable to AWS or cloud storage options'''
    if os.path.isfile(zip_path):
        zarr_store = zarr.DBMStore(zip_path, open=bsddb3.btopen)
    else:
        zarr_store = zarr.DBMStore(zip_path, open=bsddb3.btopen)
    return zarr_store

def get_files(bucketname, prefixname, textstring):
    '''Gets Files list from AWS based on a bucket name and prefix'''
    wselist = []
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name=bucketname)
    FilesNotFound = True
    for obj in bucket.objects.filter(Prefix=prefixname):
        if textstring in str(obj) and 'xml' not in str(obj):
            #print('{0}:{1}'.format(bucket.name, obj.key))
            wselist.append('{0}:{1}'.format(bucket.name, obj.key))
        FilesNotFound = False
    if FilesNotFound:
        print("ALERT", "No file in {0}/{1}".format(bucket, prefixname))
    return sorted(wselist)

def s3Attributes(s3path:str, replace_str:str='', rtype='') -> any:
    '''Creates the S3 object to write the Zarr file to the AWS bucket'''
    s3 = boto3.resource('s3')
    parent = s3path.split(':')[0]
    name = s3path.split(':')[1].split('//')[-1].replace(replace_str,'')
    s3path = s3.Object(s3path.split(':')[0], s3path.split(':')[1])
    if rtype == 'NAME': return name
    elif rtype == 'PARENT': return parent
    elif rtype == 'S3PATH': return s3path
    else: return parent, name, s3path

def SplitAndGetRemainder(r_size:int,c_groups:int):
    '''Splits the number based on a certain size and returns the rounded division and remainder'''
    _step = int(math.floor(r_size/c_groups))
    _residual = r_size - (_step * c_groups)
    return _step, _residual

def GetTifProperties_Print(ras,wse_name,num_of_chunks,total_chunks,xsize,xstep,xresidual,ysize,ystep,yresidual,print_info,proj_exist,cell_size,unit_type):
    '''Prints the Tif Properties if needed. Creates a markdown table.'''
    if print_info: mprint(f'## WSE: {wse_name}\n\nNumber of row & column chunks = {num_of_chunks}')
    if proj_exist:
        prj = ras.GetProjection()
        srs = osr.SpatialReference(wkt=prj)
        unit_type = srs.GetAttrValue('UNIT')
        if print_info: mprint(f'Cell Size: {cell_size} ({unit_type})')
    results_tbl = f"""| -           | Total   | Chunk Size | Remainder   |
                      |:-----------:|:-------:|:----------:|:-----------:|
                      | Columns (x) | {xsize} | {xstep}    | {xresidual} |
                      | Rows (y)    | {ysize} | {ystep}    | {yresidual} |"""
    if print_info:
        mprint(results_tbl)
        mprint(f'Typical Chunk Size: {ystep}x{xstep}</br>Total number of chunks: {total_chunks} (including residuals)')
    return None

def GetTifProperties(wse_name:str,s3path:any,num_of_chunks:int=10,print_info:bool=True,proj_exist:bool=True) -> tuple:
    '''Gets a number of properties from the TIf for writing the to the Zarr file'''
    rb, gt, ras = getRasData(s3path)
    cell_size, xsize, ysize = gt[1], rb.XSize, rb.YSize
    xstep, xresidual = SplitAndGetRemainder(xsize,num_of_chunks)
    ystep, yresidual = SplitAndGetRemainder(ysize,num_of_chunks)
    xadd, yadd = 1 if xresidual else 0, 1 if yresidual else 0
    total_chunks = (num_of_chunks + xadd) * (num_of_chunks + yadd)
    cell_size = cell_size if 'cell_size' in locals() else ''
    unit_type = unit_type if 'unit_type' in locals() else ''
    # Print Results if True
    GetTifProperties_Print(ras,wse_name,num_of_chunks,total_chunks,xsize,xstep,xresidual,ysize,ystep,yresidual,print_info,proj_exist,cell_size,unit_type)
    # Return Tif Properties
    return xsize, xstep, ysize, ystep, yresidual, xresidual, total_chunks

def GetTifProperties_xyn_Print(ras,wse_name,xn,yn,total_chunks,xsize,ysize,xy_size,xresidual,yresidual,print_info,proj_exist,cell_size,unit_type):
    '''Prints the Tif Properties if needed. Creates a markdown table.'''
    if print_info: mprint(f'## WSE: {wse_name}')
    if proj_exist:
        prj = ras.GetProjection()
        srs = osr.SpatialReference(wkt=prj)
        unit_type = srs.GetAttrValue('UNIT')
        if print_info: mprint(f'Cell Size: {cell_size} ({unit_type})')
    results_tbl = f"""| -           | Total   |Number of..| Chunk Size   | Remainder   |
                      |:-----------:|:-------:|:---------:|:------------:|:-----------:|
                      | Columns (x) | {xsize} | {xn}      | {xy_size}    | {xresidual} |
                      | Rows (y)    | {ysize} | {yn}      | {xy_size}    | {yresidual} |"""
    if print_info:
        mprint(results_tbl)
        mprint(f'Typical Chunk Size: {xy_size}x{xy_size}</br>Total number of chunks: {total_chunks} (including residuals)')
    return None

def GetTifProperties_xyn(wse_name:str,s3path:any,xy_size:int,print_info:bool=True,proj_exist:bool=True) -> tuple:
    '''Gets a number of properties from the TIf for writing the to the Zarr file'''
    rb, gt, ras = getRasData(s3path)
    cell_size, xsize, ysize = gt[1], rb.XSize, rb.YSize
    xn, xresidual = SplitAndGetRemainder(xsize,xy_size)
    yn, yresidual = SplitAndGetRemainder(ysize,xy_size)
    xadd, yadd = 1 if xresidual else 0, 1 if yresidual else 0
    total_chunks = (xn + xadd) * (yn + yadd)
    cell_size = cell_size if 'cell_size' in locals() else ''
    unit_type = unit_type if 'unit_type' in locals() else ''
    # Print Results if True
    GetTifProperties_xyn_Print(ras,wse_name,xn,yn,total_chunks,xsize,ysize,xy_size,xresidual,yresidual,print_info,proj_exist,cell_size,unit_type)
    # Return Tif Properties
    return xsize, xn, ysize, yn, yresidual, xresidual, total_chunks

def GetChunkAsArray(rb:any, xstart:int, ystart:int, cols:int, rows:int, boolize:bool=False):
    '''Gets the designated chunk of a TIF based on certain parameters '''
    chunk = rb.ReadAsArray(xstart, ystart, cols, rows) #start x, start y, x shape, y shape
    nullval = -9999
    if boolize: chunk[chunk != nullval] = 1
    if boolize: chunk[chunk == nullval] = 0
    return chunk

def getRasData(s3path):
    '''Finds the Ras Data from the AWS and returns GDAL Objects'''
    image_data = BytesIO(s3path.get()['Body'].read())
    tif_inmem = "/vsimem/wse.tif" #Virtual Folder to Store Data
    gdal.FileFromMemBuffer(tif_inmem, image_data.read())
    ras = gdal.Open(tif_inmem)  
    rb, gt = ras.GetRasterBand(1), ras.GetGeoTransform()
    return rb, gt, ras

def DetermineSysMemory():
    '''Determines the system free memory. Returns a readable string and raw bytes free'''
    magnitudes = {'1':'B','2':'KB','3':'MB','4':'GB','5':'TB','6':'PB'}
    available = int(str(psutil.virtual_memory()).split(', ')[1].split('=')[1])
    mem_num = '{:,}'.format(available)
    ordersofmag = str(len(mem_num.split(',')))
    currentmag = magnitudes[ordersofmag]
    mainnum = mem_num.split(',')[0]
    subnum = math.floor(int(mem_num.split(',')[1])/100)
    #memoryfinal = int(float(f"{mainnum}.{subnum}")*(10**(int(ordersofmag)*3-3)))
    return f"{mainnum}.{subnum} {currentmag}", available

def getMagnitude(sizeofdata):
    '''Return the data Size of a `sys.getsizeof({object})` for any python object'''
    magnitudes = {'1':'B','2':'KB','3':'MB','4':'GB','5':'TB','6':'PB'}
    mem_used = '{:,}'.format(sizeofdata)
    ordersofmag = str(len(mem_used.split(',')))
    currentmag = magnitudes[ordersofmag]
    mainnum = mem_used.split(',')[0]
    subnum = math.floor(int(mem_used.split(',')[1])/100)
    return f"{mainnum}.{subnum} {currentmag}", sizeofdata

def FindGDALtype(rb_DataType):
    '''Found from Help in GDAL with help()'''
    NP2GDAL_CONVERSION = {"uint8": 1,"int8": 1,"uint16": 2,"int16": 3,"uint32": 4,"int32": 5,
                          "float32": 6,"float64": 7,"complex64": 10,"complex128": 11}
    gtype = ''
    for key in NP2GDAL_CONVERSION.keys():
        result = NP2GDAL_CONVERSION[key]
        if result == rb_DataType:
            gtype = key
    if gtype != '': return gtype
    else: return 'GDAL TYPE NOT FOUND'

def GDALtypeToDtype(gtype):
    '''returns the Numpy version of GDALs data type for Zarr compatibility;
    https://docs.scipy.org/doc/numpy-1.15.1/reference/arrays.dtypes.html'''
    GDALtoDconversion = {"uint8":'u1',"int8":'i1',"uint16":'u2',"int16":'i2',"uint32":'u4',
                         "int32":'i4',"float32":'f4',"float64":'f8',"complex64":'c8',
                         "complex128":'c16','GDAL TYPE NOT FOUND':'ERROR'}
    np_dtype =  GDALtoDconversion[gtype]
    return np_dtype

def IsFreeMemoryEnough(xsize,ysize,datasize=5):
    '''Checks to see if the current free memory can handle the tif as one object.
    If True, then it returns the xy sizes with True. Else, it returns the safest and largest 
    chunk size as a square.'''
    mem_str, mem_free = DetermineSysMemory()
    csize = xsize*ysize
    mem_size = (mem_free-112)/datasize
    ismemenough = (mem_size>=csize)
    if ismemenough:
        return xsize, ysize, ismemenough
    else:
        new_size = math.floor((mem_size**0.5)/10.0)*10
        return new_size, new_size, ismemenough

def getGTExtents(gt,xsize,ysize):
    xmin, ymax = gt[0], gt[3]
    xmax = xmin + (gt[1]*xsize)
    ymin = ymax + (gt[5]*ysize)
    return {"XMIN":xmin, "YMIN":ymin, "XMAX":xmax, "YMAX":ymax}

def getFullRASMetaData(ras,gt,rb,xsize,ysize):
    prj = ras.GetProjection()
    srs = osr.SpatialReference(wkt=prj)
    unit_type = srs.GetAttrValue('UNIT')
    extents = getGTExtents(gt,xsize,ysize)
    rb.GetStatistics(True, True)
    stats_meta = rb.GetMetadata()
    cell_size, xsize, ysize =  gt[1], rb.XSize, rb.YSize
    meta_dict = {"Cell Size":cell_size,
                 "Extents":extents,
                 "Full GetStatistics":stats_meta,
                 "Projection":prj,
                 "Unit Type":unit_type,
                 "XYSize":(xsize, ysize)}
    return meta_dict

def GetChunkMetaData(gt,xsize,ysize,row_nm,col_nm,cell_size):
    extents = getGTExtents(gt,xsize,ysize)
    XMIN, YMAX = extents['XMIN'], extents['YMAX']
    chunk_xmin = XMIN + (int(col_nm))*cell_size
    chunk_ymax = YMAX - (int(row_nm))*cell_size
    chunk_xmax = chunk_xmin + xsize*cell_size
    chunk_ymin = chunk_ymax - ysize*cell_size
    chunk_meta_dict = {"XMIN":chunk_xmin, "YMIN":chunk_ymin, "XMAX":chunk_xmax, "YMAX":chunk_ymax}
    return chunk_meta_dict

def CreateFullZarrArray(z,obj_name,rb,xsize,ysize,boolize):
    model_group = z.create_group(f'{obj_name}', overwrite=True)
    chunk = GetChunkAsArray(rb, 0, 0, xsize, ysize, boolize)
    model_group.create_dataset(f'Chunk_{row_nm}_{col_nm}', data=chunk, shape=(xsize,ysize), overwrite=True, dtype=np_dtype)
    z.attrs[f'{obj_name}'] = getFullRASMetaData(ras,gt,rb,xsize,ysize)
    #model_group.attrs[f'Chunk_{row_nm}]
    return z

def StoreTifInZarr_SquareChunks(s3tif:path,zarr_file:path,pathname:str,boolize:bool=False,datatype:any=False,pruntime:bool=False):
    '''Create the Zarr File, Groups, and Datasets'''
    start_time = time.time()
    zwse_store = s3fs.S3Map(root=zarr_file, s3=s3fs.S3FileSystem(), check=False)
    obj_parent, obj_name, obj_s3path = s3Attributes(s3tif, '.tif')
    obj_name = obj_name.split('/')[-1]
    rb, gt, ras = getRasData(obj_s3path)
    cell_size, xsize, ysize, np_dtype = gt[1], rb.XSize, rb.YSize, GDALtypeToDtype(FindGDALtype(rb.DataType))
    if datatype: # Change Datatype only if needed.
        np_dtype = datatype
    xsize, ysize, ismemenough = IsFreeMemoryEnough(xsize, ysize)
    z = zr.group(store=zwse_store,path=pathname,overwrite=True)
    if ismemenough:
        model_group = z.create_group(f'{obj_name}', overwrite=True)
        row_nm, col_nm = '0', '0'
        chunk = GetChunkAsArray(rb, 0, 0, xsize, ysize, boolize)
        model_group.create_dataset(f'Chunk_{row_nm}_{col_nm}', data=chunk, shape=(xsize,ysize), overwrite=True, dtype=np_dtype)
        z.attrs[f'{obj_name}'] = getFullRASMetaData(ras,gt,rb,xsize,ysize)
        model_group.attrs[f'Chunk_{row_nm}_{col_nm}'] = GetChunkMetaData(gt,xsize,ysize,row_nm,col_nm,cell_size)
    else:
        xy_size = xsize 
        xsize, xn, ysize, yn, yresidual, xresidual, total_chunks = GetTifProperties_xyn(obj_name,obj_s3path,xy_size,print_info=True,proj_exist=True)
        model_group = z.create_group(f'{obj_name}', overwrite=True)
        z.attrs[f'{obj_name}'] = getFullRASMetaData(ras,gt,rb,xsize,ysize)
        gc_sigfig = len(str(max([xn,yn])))
        for j in range(yn): #tracking through rows
            row_nm = ('{'+f':0{gc_sigfig}'+'d}').format(j)
            for k in range(xn): # Tracking through columns
                col_nm = ('{'+f':0{gc_sigfig}'+'d}').format(k)
                chunk = GetChunkAsArray(rb, xy_size*k, xy_size*j, xy_size, xy_size, boolize)   
                model_group.create_dataset(f'Chunk_{row_nm}_{col_nm}', data=chunk, shape=(xy_size,xy_size), overwrite=True, dtype=np_dtype)
                model_group.attrs[f'Chunk_{row_nm}_{col_nm}'] = GetChunkMetaData(gt,xy_size,xy_size,row_nm,col_nm,cell_size)
            if xresidual:
                col_nm = 'R'
                chunk = GetChunkAsArray(rb, xy_size*k+1, xy_size*j, xresidual, xy_size, boolize)      
                model_group.create_dataset(f'Chunk_{row_nm}_{col_nm}', data=chunk, shape=(xresidual,xy_size), overwrite=True, dtype=np_dtype)
                model_group.attrs[f'Chunk_{row_nm}_{col_nm}'] = GetChunkMetaData(gt,xy_size,xy_size,row_nm,col_nm,cell_size)
        if yresidual:
            row_nm = 'R'
            for k in range(xn):
                col_nm = ('{'+f':0{gc_sigfig}'+'d}').format(k)
                GetChunkAsArray(rb, xy_size*k, xy_size*j+1, xy_size, yresidual, boolize)      
                model_group.create_dataset(f'Chunk_{row_nm}_{col_nm}', data=chunk, shape=(xy_size,yresidual), overwrite=True, dtype=np_dtype)
                model_group.attrs[f'Chunk_{row_nm}_{col_nm}'] = GetChunkMetaData(gt,xy_size,xy_size,row_nm,col_nm,cell_size)
            if xresidual: #print('R','R')
                col_nm = 'R'
                GetChunkAsArray(rb, xy_size*k+1, xy_size*j+1, xresidual, yresidual, boolize)     
                model_group.create_dataset(f'Chunk_{row_nm}_{col_nm}', data=chunk, shape=(xresidual,yresidual), overwrite=True, dtype=np_dtype)
                model_group.attrs[f'Chunk_{row_nm}_{col_nm}'] = GetChunkMetaData(gt,xy_size,xy_size,row_nm,col_nm,cell_size)
    run_time = (time.time()-start_time)/60
    if pruntime: mprint('## Total Runtime: {:0.2f} Minutes'.format(run_time))
    return z