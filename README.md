# NDVI Python Script

A simple python script for calculating NDVI values from Earth Observation data. Works with rasterio and numpy libraries.

## Terminal arguments:

-p or --path: Path to data.\
-r or --red_band: Name of the red band image.\
-n or --nir_band: Name of the NIR band image.\
-o or --output: Name of the output image.

## Examples:

#### $python3 NDVI.py -r L2A_T34SEJ_20170228T092021_B04_10m.jp2 -n L2A_T34SEJ_20170228T092021_B08_10m.jp2 -p . -o L2A_T34SEJ_20170228T092021_ndvi.tif

#### $python3 NDVI.py -r L2A_T34SEJ_20170228T092021_B04_10m.jp2 -n L2A_T34SEJ_20170228T092021_B08_10m.jp2 -p .
