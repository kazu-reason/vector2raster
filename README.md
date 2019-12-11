# vector2raster
> Converting vector to raster with specified color for map tile layer

- Vector: only support for geojson now
- Raster: only support for geojson now
- geojson feature: only support for `Polygon` or `MultiPolygon` now

## Requirements
Using pipenv for virtualenv and package management
```bash
$ pip install pipenv
```

## Usage
### Preparation
```bash
# copy .env_template, setting_template.py and edit
# $ cp .env_template .env
$ cp setting_template.py setting.py

# pipenv preparation
$ pipenv sync
```

### Convert from geojson
<!-- To receive geojson, you have to specify the geojson server in `.env`. -->
To receive geojson, you have to specify the geojson server in `setting.py`.

```bash
# start server
$ pipenv run start
```

### Convert from mbtiles
```bash
# enter to the pipenv
$ pipenv shell
# file to file conversion
$ python geojsonDict2png.py your_mbtiles output.png z x y
```

## Feature work
- Support mbtiles with pbf(mvt) tiles for input
- Support mbtiles with png tiles for output
- Support styling(coloring) depends on
  - attribute
  - reference tabel to decide coloring with `KEY_CODE`
    - csv 
    - DB
- Support more geojson feature types
- Change library from Pillow to Pillow-SIMD
  - https://qiita.com/koshian2/items/c26656a565e42093069d
