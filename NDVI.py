# NDVI Python Script
#
# GNU GENERAL PUBLIC LICENSE
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Created by Alexandros Falagas
#
from osgeo import gdal
# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()
from gdalconst import *
import numpy as np
red=gdal.Open("red.tif", GA_ReadOnly)
if red is None:
	print 'Could not open file'
	sys.exit(1)
r=np.array(red.GetRasterBand(1).ReadAsArray(), dtype=float)
nir=gdal.Open("nir.tif", GA_ReadOnly)
if nir is None:
	print 'Could not open file'
	sys.exit(1)
n=np.array(nir.GetRasterBand(1).ReadAsArray(), dtype=float)
geotr=red.GetGeoTransform()  
proj=red.GetProjection()   
tableshape=r.shape
np.seterr(divide='ignore', invalid='ignore') #Ignore the divided by zero or Nan appears
ndvi=(n-r)/(n+r) # The NDVI formula
driver = gdal.GetDriverByName("GTiff")
dst_ds = driver.Create("ndvi.tif", tableshape[1], tableshape[0], 1, gdal.GDT_Float32)
dst_ds.SetGeoTransform(geotr)
dst_ds.SetProjection(proj)
dst_ds.GetRasterBand(1).WriteArray(ndvi)
dst_ds = None  # save, close
print "The NDVI image is saved."
