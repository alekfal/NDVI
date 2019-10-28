# NDVI Python Script\n
\n
A simple python script for calculating NDVI values from Earth Observation data. Works with rasterio and numpy libraries.\n
\n
## Terminal arguments:\n
\n
-p or --path: Path to data.\n
-r or --red_band: Name of the red band image.\n
-n or --nir_band: Name of the NIR band image.\n
-o or --output: Name of the output image.\n
\n
## Examples:\n
\n
#### 1: $python3 NDVI.py -r L2A_T34SEJ_20170228T092021_B04_10m.jp2 -n L2A_T34SEJ_20170228T092021_B08_10m.jp2 -p . -o L2A_T34SEJ_20170228T092021_ndvi.tif

#### 2: $python3 NDVI.py -r L2A_T34SEJ_20170228T092021_B04_10m.jp2 -n L2A_T34SEJ_20170228T092021_B08_10m.jp2 -p .
