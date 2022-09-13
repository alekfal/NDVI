# NDVI Python Script

A simple python script for calculating NDVI values from earth observation multispectral data. Rasterio and numpy libraries are required.

## Installation

Clone the repository and install the required libraries using ```pip```:

```bash
git clone https://github.com/alekfal/NDVI.git
cd NDVI/
pip install -r requirements.txt
```

## Terminal arguments


| Short options | Long options     | Description                   | Required |
|---------------|------------------|-------------------------------|----------|
|```-p```       | ```--path```     | Path to data                  | Yes      |
|```-r```       | ```--red_band``` | Name of the red band image    | Yes      |
| ```-n```      | ```--nir_band``` | Name of the NIR band image    | Yes      |
| ```-o```      | ```--output```   | Name of the output image      | No       |


## Examples

```bash
python NDVI.py -p . -r red_image.tif -n nir_image.tif -o my_new_ndvi_image.tif
python NDVI.py -p . -r red_image.tif -n nir_image.tif
```
