# Title: Read a raster with rasterio
# Name: Falagas Alekos
# Location: RSLab, SRSE-NTUA, 2019
# e-mail: alek.falagas@gmail.com
# Version: 0.0.4

"""
Latest Update:

1. writeraster is checking for datatypes based on user's input and array's datatype.
2. New function datatypes added.

"""

import rasterio
import os
import sys
import numpy as np


def datatypes(dtp):
    """
    This function return the code of the datatype.
    Input:
        dtp - Input datatype (string)
    Output:
        dtype[dtp] - Code (int)
    """

    # Dictionary with GDT datatypes and their codes
    dtype_fwd = {None: 0, #GDT_Unknown
        'uint8': 1, #GDT_Byte
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

    return (dtype_fwd[dtp])

def metadata(path, name,  verbose = False):
    """
    A simple function to read raster file metadata.
    Inputs:
        * path - Path to raster file (string)
        * name - Name of the raster file (string)
        * verbose - Printing results (Optional, default value = False) (bool)
    Outputs:
        * crs - Coordinates Reference System (String)
        * bands - Number of bands (Integer)
        * up_l_crn - Upper left corner coordinates (Tuple)
        * pixel_size - Pixel size (Integer)
        * width - Number of columns (Integer)
        * height - Number of rows (Integer)
        * dtps - Image's datatype (Tuple)
        * dtp_code - Datatype's code (Tuple)
        * driver - Image's driver (String)
        * utm - Image's CRS in WKT (String)
        * transform - Image's transform (Tuple)
    """

    # Reading image
    image = rasterio.open(os.path.join(path, name))

    # Getting CRS
    crs = image.crs

    # Counting bands
    bands = image.count

    # Getting transform
    transform = image.transform

    # Upper left corner
    up_l_crn = image.transform * (0, 0)
    
    # Getting pixel size
    pixel_size = image.transform[0]
    
    # Getting width and height
    width = image.width
    height = image.height

    # Working with datatypes
    dtps = image.dtypes
    # Empty list for adding codes 
    dtp_code = []
    for dtp in dtps:
        dtp_code.append(datatypes(dtp))
        if verbose == True:
            print ('Data Type: {} - {}'.format(dtp, dtp_code))
    # Getting driver
    driver = image.driver
    
    # Getting CRS as Well Known Text
    utm = crs.wkt

    # Print results if True
    if verbose == True:
        print ('CRS: {}'.format(crs))
        print ('Bands: {}'.format(bands))
        print ('Upper Left Corner: {}'.format(up_l_crn))
        print ('Pixel size: {}'.format(pixel_size))
        print ('Width: {}'.format(width))
        print ('Height: {}'.format(height))
        print (driver)
        print ('UTM Zone: {}'.format(utm))

    return (crs, bands, up_l_crn, pixel_size, width, height, dtps, dtp_code, driver, utm, transform)

def readraster(path, name, bands = -1):
    """
    A simple function to read raster files. Uses function metadata() for getting information about the image.
    Inputs:
        * path - Path to raster file (string)
        * name - Name of the raster file (string)
        * bands - Default values: bands = -1 (read all bands). For reading for example the first 2 bands of a
          multiband use variable bands as: bands = (1, 2). To read 1 band just provide the corresponding band number
    Outputs:
        * image - The image as a rasterio object
        * array - The image as a np.array
        * all the metadata from function metadata()
    """

    print ('Trying to read raster file...')
    print ('Reading file {}.'.format(name))
    
    # Getting metadata
    crs, count, up_l_crn, pixel_size, width, height, dtps, dtp_code, driver, utm, transform = metadata(path, name)

    # Reading data with rasterio
    image = rasterio.open(os.path.join(path, name))

    # Getting all bands as np.arrays
    if bands == -1:
            array = image.read()
    # Read specific bands
    else:
        array = image.read(bands)
    
    print ('Done!')

    return (image, array, crs, count, up_l_crn, pixel_size, width, height, dtps, dtp_code, driver, utm, transform)

def writeraster(path, name, array, width, height, crs, transform, dtype = (rasterio.float32,), ext = 'Gtiff'):
    """
    Write a new raster with rasterio.
    Inputs:
        * path - Path to raster file (string)
        * name - Name of the raster file (string)
        * array - The image as a np.array (np.array)
        * width - Number of columns (Integer)
        * height - Number of rows (Integer)
        * crs - Coordinates Reference System (String)
        * transform - Image transform (Tuple)
        * dtype - Image datatype (Optional, default value = (rasterio.float32,)). In case of difference in array's datatype and user's datatype
          the script will save data with array's datatype (tuple)
        * ext - Extension (Optional, default value = 'Gtiff') (string)
    Outputs:
        * Raster file to selected path 
    """

    print ('Trying to write raster data...')
    
    # Checking if there are more than 1 dtypes and dtype is a list
    if len(dtype) > 0 and isinstance(dtype, tuple):
        # Checking for unique values in case of multiband image
        unique = list(set(dtype))
        if len(unique) > 0:
            fdtype = unique[0]
            for u in unique:
                if datatypes(fdtype) < datatypes(u):
                    fdtype = u
        else:
            fdtype = dtype
    else:
        print ('Something is wrong with datatypes. Try to use readraster(...) to open the image.')
        sys.exit(1)

    #Checking if user's datatype matches with array's datatype
    if len(array.shape) == 3:
        for i in range(len(array)):
            if array[i, :, :].dtype != fdtype:
                print ("Found difference in array's datatype and user's datatype.")
                print ("Replacing datatype {} with {}.".format(fdtype, array[i, :, :].dtype))
                fdtype = array[i, :, :].dtype
    else:
         if array.dtype != fdtype:
            print ("Found difference in array's datatype and user's datatype.")
            print ("Replacing datatype {} with {}.".format(fdtype, array.dtype))
            fdtype = array.dtype

    # Multiband images
    if len(array.shape) == 3:
        bands=rasterio.open(os.path.join(path, name),'w',driver=ext,width=width, height=height,
            count = len(array),
            crs = crs,
            transform = transform,
            dtype = fdtype)
        for b in range(len(array)):
            bands.write(array[b,:,:], b+1)
        bands.close()
    # Singleband image
    else:
        bands=rasterio.open(os.path.join(path, name),'w',driver=ext,width=width, height=height,
            count = 1,
            crs = crs,
            transform = transform,
            dtype = fdtype)
        bands.write(array, 1)
        bands.close()
    print ('Raster saved as {}.'.format(name))

def split_bands(path, name, name_ext = '_band_', verbose = False):
    """
    A simple function to split multiband raster data to single images.
    Inputs:
        * path - Path to raster file (string)
        * name - Name of the raster file (string)
        * name_ext - New name extension (Optional, default value = '_band_') (string)
        * verbose - Printing results (Optional, default value = False) (bool)
    Outputs:
        * Raster files to selected path
    """

    # Reading data with rasterio
    image = rasterio.open(os.path.join(path, name))
    
    # Getting image name without extension
    name_we = os.path.splitext(name)[0]
    
    # Loop to all bands
    for b in range(1, (image.count+1)):

        # New name
        filename = name_we + '{}{}.tif'.format(name_ext, b)
        if verbose == True:
            print ('Trying to save band {} as {}'.format(b, filename))
        # Write new raster
        band=rasterio.open(filename, 'w', driver = 'Gtiff', width = image.width, height=image.height, count = 1, 
            crs = image.crs, transform = image.transform, dtype=image.read(b).dtype)
        band.write(image.read(b), 1)
        band.close()
        if verbose == True:
            print('Done!')
