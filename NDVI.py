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
# Last update 13-09-2022

import sys
import os
import optparse
import numpy as np
import rasterio

class OptionParser (optparse.OptionParser):
	"A class to parse the arguments."
	
	def check_required (self, opt):
		"A simple method to check the required parameters."
		
		option = self.get_option(opt)
		# Assumes the option's 'default' is set to None!
		if getattr(self.values, option.dest) is None:
			self.error("{} option is required.".format(option))

def NDVI(r:np.array, n:np.array)->np.array:
	"""The NDVI function.

	Args:
		r (np.array): Red band array
		n (np.array): NIR band array

	Returns:
		np.array: NDVI array
	"""
	np.seterr(divide='ignore', invalid='ignore') # Ignore the divided by zero or Nan appears
	# BE CAREFULL! Without this convertion, doesn't work correctly !
	n = n.astype(rasterio.float32)
	r = r.astype(rasterio.float32)
	ndvi = (n - r) / (n + r) # The NDVI formula

	return ndvi

if __name__ == "__main__":
	# Parse command line arguments.
	if len(sys.argv) == 1:
		prog = os.path.basename(sys.argv[0])
		print ('      '+sys.argv[0]+' [options]')
		print ("For more information try: python3 ", prog, " --help")
		print ("or: python3 ", prog, " -h")
		print ("example python3  {} --red_band red.tif --nir_band nir.tif --path .".format(sys.argv[0]))
		print ("example python3  {} --red_band red.tif --nir_band nir.tif --path . --output ndvi.tif".format(sys.argv[0]))
		sys.exit(-1)
	else:
		usage = "usage: %prog [options] "
		parser = OptionParser(usage=usage)
		parser.add_option("-r", "--red_band", dest = "red", action = "store", type = "string", help = "Name of the red band image.", default = None)
		parser.add_option("-n", "--nir_band", dest = "nir", action = "store", type = "string", help = "Name of the nir band image.", default = None)
		parser.add_option("-p", "--path", dest = "path", action = "store", type = "string", help = "Path to data.", default = None)
		parser.add_option("-o", "--output", dest="output", action = "store", type="string", help="Name of the output image.", default=None)

		(options, args) = parser.parse_args()

		# Checking required arguments for the script.
		parser.check_required("-r")
		parser.check_required("-n")
		parser.check_required("-p")

		if options.output == None:
			name = "NDVI.tif"
		else:
			name = options.output
		


		# Reading red band.
		red = rasterio.open(os.path.join(options.path, options.red), "r")
		red_array = red.read()
		metadata = red.meta.copy()
		
		# Reading NIR band
		nir = rasterio.open(os.path.join(options.path, options.nir), "r")
		nir_array = nir.read()

		# Calling the NDVI function.
		ndvi_array = NDVI(red_array, nir_array)
		
		# Updating metadata
		metadata.update({"driver":"GTiff", "dtype": rasterio.float32})		

		# Writing the NDVI raster with the same properties as the original data
		with rasterio.open(os.path.join(options.path, name), "w", **metadata) as dst:
			if ndvi_array.ndim == 2:
				dst.write(ndvi_array, 1)
			else:
				dst.write(ndvi_array)
			