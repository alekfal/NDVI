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
# Last update 28-09-2019

import sys
import os
import optparse
import numpy as np

from earthobspy import readraster, writeraster

class OptionParser (optparse.OptionParser):
	"A class to parse the arguments."
	
	def check_required (self, opt):
		"A simple method to check the required parameters."
		
		option = self.get_option(opt)
		# Assumes the option's 'default' is set to None!
		if getattr(self.values, option.dest) is None:
			self.error("{} option is required.".format(option))

def NDVI(r, n):
	"The NDVI function."

	np.seterr(divide='ignore', invalid='ignore') #Ignore the divided by zero or Nan appears
	ndvi = (n-r)/(n+r) # The NDVI formula
	ndvi = np.float32(ndvi) # Convert datatype to float32 for memory saving.
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
		parser.add_option("-o", "--output", dest="output", action="store", type="string", help="Name of the output image.",default=None)

		(options, args) = parser.parse_args()

		# Checking required arguments for the script.
		parser.check_required("-r")
		parser.check_required("-n")
		parser.check_required("-p")

		if options.output == None:
			name = "NDVI_IMAGE.tif"
		else:
			name = options.output
		# Reading red band.
		(image, red, crs, count, up_l_crn, pixel_size, width, height, dtps, dtp_code, driver, utm, transform) = readraster(options.path, options.red)
		# Reading NIR band.
		(image, nir, crs, count, up_l_crn, pixel_size, width, height, dtps, dtp_code, driver, utm, transform) = readraster(options.path, options.nir)
		# Calling the NDVI function.
		ndvi = NDVI(red, nir)
		# Writing the NDVI raster with the same properties as the original data
		writeraster(options.path, name, ndvi, width, height, crs, transform, ['float32'], ext = 'Gtiff')
