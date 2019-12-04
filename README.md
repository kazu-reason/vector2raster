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
```bash
# copy .env template and edit
$ cp .env_template .env

# pipenv preparation
$ pipenv sync
$ pipenv run start
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
