import sys
import random
import itertools
from math import pi, e, atan
from PIL import Image, ImageDraw, ImageOps
import geopandas as gpd
import shapely

FIG_SIZE = 256

def geojson2png(df_gpd=None, tile_z=0, tile_x=0, tile_y=0, FIG_SIZE=FIG_SIZE):
    """create png data from geojson data

    create png data from geojson data(geopandas)

    Parameters
    ----------
    df_gpd : geopandas.DataFrame
        source data for creating raster image
    tile_z : int
        tile z coords
    tile_x : int
        tile x coords
    tile_y : int
        tile y coords
    FIG_SIZE : int
        raster image size

    Returns
    -------
    PIL.Image.Image
        raster image data(Pillow format)
            
    """

    # initialize
    tile_x, tile_y, tile_z = int(tile_x), int(tile_y), int(tile_z)
    im = Image.new("RGB", (FIG_SIZE, FIG_SIZE), 0)
    draw = ImageDraw.Draw(im)

    
    def tile2latlon(x, y, z):
        lon = (x / 2.0**z) * 360 - 180
        mapy = (y / 2.0**z) * 2 * pi - pi
        lat = 2 * atan(e ** (- mapy)) * 180 / pi - 90
        return (lon, lat) # (x, y) = (経度, 緯度)

    # get tile's left upper(north west) coords
    x_min, y_max = tile2latlon(tile_x, tile_y, tile_z)
    # get tile's right lower(south east) coords
    x_max, y_min = tile2latlon(tile_x+1, tile_y+1, tile_z)

    def append_coords_to_list(coords, target_x_list, target_y_list):
        geom_x = list(coords[0])
        geom_y = list(coords[1])
        geom_x_list.append(geom_x)
        geom_y_list.append(geom_y)


    def position_in_image(geom_x, geom_y):
        image_x = (geom_x - x_min) / (x_max - x_min) * FIG_SIZE
        image_y = (geom_y - y_min) / (y_max - y_min) * FIG_SIZE

        return (image_x, image_y)


    # variables for loop
    func_ACTL = append_coords_to_list
    geom_x_list = []
    geom_y_list = []
    MultiLineStringClass = shapely.geometry.multilinestring.MultiLineString

    for idx in range(0,len(df_gpd)):
        geom = df_gpd.iloc[idx]["geometry"]
        if type(geom.boundary) is MultiLineStringClass:
            for g in geom.boundary:
                coords = g.coords.xy
                func_ACTL(coords, geom_x_list, geom_y_list)
        else:
            coords = geom.boundary.coords.xy
            func_ACTL(coords, geom_x_list, geom_y_list)

    # draw polygons from geom_x_list, geom_y_list
    func_PII = position_in_image
    for idx in range(0,len(geom_x_list)):
        rand_tuple = (55+random.randint(0,200),55+random.randint(0,200),55+random.randint(0,200))

        geom_pair = [(geom_x_list[idx][i], geom_y_list[idx][i]) for i in range(0, len(geom_x_list[idx]))]        
        geom_pair_fixed = [func_PII(*geom_pair[i]) for i in range(0, len(geom_pair))]
        draw.polygon(xy=geom_pair_fixed, fill=rand_tuple)

    # flip because 
    # Pillow's      axis origin is left upper side
    # x/y/z tile's  axis origin is left lower side
    im_flip = ImageOps.flip(im)
    # set alpha value if needed
    # im_flip.putalpha(128)
    return im_flip


def geojson_file2png_file(inputFilePath=None, outputFilePath=None, tile_z=0, tile_x=0, tile_y=0, FIG_SIZE=FIG_SIZE):
    """output png file from geojson file

    Parameters
    ----------
    inputFilePath : str
        source data file path(geojson)
    outputFilePath : str
        output data file path(png)
    tile_z : int
        tile z coords
    tile_x : int
        tile x coords
    tile_y : int
        tile y coords
    FIG_SIZE : int
        raster image size
            
    """

    df_gpd = gpd.read_file(inputFilePath) # geojson -> geopandas.DataFrame
    im = geojson2png(df_gpd, tile_z, tile_x, tile_y, FIG_SIZE)
    im.save(outputFilePath) # イメージ出力


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("filePath is not specified")
    else:
        geojson_file2png_file(
            sys.argv[1], sys.argv[2], # path args
            sys.argv[3], sys.argv[4], sys.argv[5] # z/x/y args
        )