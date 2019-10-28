# Title: Read a raster with rasterio
# Name: Falagas Alekos
# Location: RSLab, SRSE-NTUA, 2019
# e-mail: alek.falagas@gmail.com
# Version: 0.0.3

import rasterio
import os
import numpy as np

def metadata(path, name,  verbose = False):
    "A simple function to read raster file metadata."

    dtype_fwd = {
        None: 0, #GDT_Unknown
        'uint8':1, #GDT_Byte
        'ubyte': 1, #GDT_Byte
        'uint16': 2, #GDT_UInt16
        'int16': 3, #GDT_Int16
        'uint32': 4, #GDT_UInt32
        'int32': 5, #GDT_Int32
        'float32': 6, #GDT_Float32
        'float64': 7, #GDT_Float64
        'complex_': 8, #GDT_CInt16
        'complex_': 9, #GDT_CInt32
        'complex64': 10, #GDT_CFloat32
        'complex128': 11} #GDT_CFloat64

    image = rasterio.open(os.path.join(path, name))
    crs = image.crs
    bands = image.count
    up_l_crn = image.transform * (0, 0)
    pixel_size = image.transform[0]
    rows = image.width
    cols = image.height
    dtps = image.dtypes
    dtp_code= []
    for dtp in dtps:
        dtp_code.append(dtype_fwd[dtp])
        if verbose == True:
            print ('Data Type: {} - {}'.format(dtp, dtp_code))
    driver = image.driver
    utm = crs.wkt

    # Print results if True
    if verbose == True:
        print ('CRS: {}'.format(crs))
        print ('Bands: {}'.format(bands))
        print ('Upper Left Corner: {}'.format(up_l_crn))
        print ('Pixel size: {}'.format(pixel_size))
        print ('Rows: {}'.format(rows))
        print ('Columns: {}'.format(cols))
        print (driver)
        print ('UTM Zone: {}'.format(utm))

    return (crs, bands, up_l_crn, pixel_size, rows, cols, dtps, dtp_code, driver, utm)

def readraster(path, name, bands = -1):
    "A simple function to read raster files."
    print ('Trying to read raster file...')
    print ('Reading file {}.'.format(name))
    # Reading data with rasterio
    image = rasterio.open(os.path.join(path, name))
    crs, count, up_l_crn, pixel_size, rows, cols, dtps, dtp_code, driver, utm = metadata(path, name)
    transform = image.transform

    # Getting all Bands
    if bands == -1:
            array = image.read()
    else:
        array = image.read(bands)
    print ('Done!')
    return (image, array, crs, count, up_l_crn, pixel_size, rows, cols, dtps, dtp_code, driver, utm, transform)

def writeraster(path, name, array, width, height, crs, transform, dtype, ext = 'Gtiff'):
    print ('Trying to write raster data...')
    # Export stacked color image

    if len(dtype) > 0:
        dtype = dtype[0]

    if len(array.shape) == 3:
        bands=rasterio.open(name,'w',driver=ext,width=width, height=height,
            count = len(array),
            crs = crs,
            transform = transform,
            dtype = dtype)
        for b in range(len(array)):
            bands.write(array[b,:,:], b+1)
        bands.close()
    else:
        bands=rasterio.open(name,'w',driver=ext,width=width, height=height,
            count = 1,
            crs = crs,
            transform = transform,
            dtype = dtype)
        bands.write(array, 1)
        bands.close()
    print ('Raster saved as {}.'.format(name))

def split_bands(path, name, verbose = False):
    "A simple function to split multiband raster data to single images"
    # Reading data with rasterio
    image = rasterio.open(os.path.join(path, name))
    # Getting image name without extension
    name_we = os.path.splitext(name)[0]
    for b in range(1, (image.count+1)):
        filename = name_we + '_band_{}.tif'.format(b)
        if verbose == True:
            print ('Trying to save band {} as {}'.format(b, filename))
        band=rasterio.open(filename,'w',driver = 'Gtiff',width = image.width, height=image.height, count = 1, crs = image.crs, transform = image.transform, dtype=image.read(b).dtype)
        band.write(image.read(b), 1) #green
        band.close()
        if verbose == True:
            print('Done!')

#Test
#split_bands('./', 'Ortho_Ziogas_SWIR_GG87.tif')
