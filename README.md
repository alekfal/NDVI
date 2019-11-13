# NDVI Python Script

A simple python script for calculating NDVI values from Earth Observation data. Works with rasterio and numpy libraries. Also for reading, writing rasters the EarthObsevation repository is used (https://github.com/alekfal/EarthObservationLibrary).

## Terminal arguments:
----------------------

```
-p or --path: Path to data.\
-r or --red_band: Name of the red band image.\
-n or --nir_band: Name of the NIR band image.\
-o or --output: Name of the output image.

```

## Examples:
----------------------

```
$python3 NDVI.py -r red_image.tif -n nir_image.tif -p . -o my_new_ndvi_image.tif

$python3 NDVI.py -r red_image.tif -n nir_image.tif -p .
```