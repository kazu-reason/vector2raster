import sys
import itertools
from math import pi, e, atan
from PIL import Image, ImageDraw, ImageOps
import shapely
from handle_mbtiles import read_tiles
from style import get_color_from_sqlite, get_color_from_postgresql, get_random_color
import setting

FIG_SIZE = 256

def geojsonDict2png(geojsonDict=None, FIG_SIZE=FIG_SIZE):
    """create png data from geojson data

    create png data from geojson data(does not use geopandas)

    Parameters
    ----------
    geojsonDict : dict
        source data for creating raster image
    FIG_SIZE : int
        raster image size
    color_src : str(default:'random')
        decide to use random coloring or specify DB to get value

    Returns
    -------
    PIL.Image.Image
        raster image data(Pillow format)
            
    """

    # initialize
    im = Image.new("RGBA", (FIG_SIZE, FIG_SIZE), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    
    # return all transparent layer for empty dataset
    if len(geojsonDict) == 0:
        return im

    dictContent = geojsonDict.get(list(geojsonDict.keys())[0])
    features = dictContent.get("features")
    extent = dictContent.get("extent")
    DPI = FIG_SIZE / extent # dot per extent
    color_src = setting.color_src
    if color_src == "sqlite":
        func_get_color = get_color_from_sqlite
    elif color_src == "postgresql":
        func_get_color = get_color_from_postgresql
    else:
        func_get_color = color_src
    

    def position_in_image(geom_x, geom_y):
        image_x = geom_x * DPI
        image_y = geom_y * DPI

        return (image_x, image_y)
    

    def polygon_loop(geometryCoords=None, draw=None, KEY_CODE=None):
        func_PII = position_in_image

        for coords_1 in geometryCoords:
            image_xy_list = []
            for coords_2 in coords_1:
                x,y = coords_2
                image_coords = func_PII(x,y)
                image_xy_list.append(image_coords)

            # draw polygons from image_xy_list
            rand_tuple = func_get_color(KEY_CODE)
            if rand_tuple != (0,0,0):
                draw.polygon(xy=image_xy_list, fill=rand_tuple)
    
    
    def multiPolygon_loop(geometryCoords=None, draw=None, KEY_CODE=None):
        func_PII = position_in_image

        for coords_1 in geometryCoords:
            for coords_2 in coords_1:
                image_xy_list = []
                for coords_3 in coords_2:
                    x,y = coords_3
                    image_coords = func_PII(x,y)
                    image_xy_list.append(image_coords)

                # draw polygons from image_xy_list
                rand_tuple = func_get_color(KEY_CODE)
                if rand_tuple != (0,0,0):
                    draw.polygon(xy=image_xy_list, fill=rand_tuple)
    

    for feature in features:
        geometry = feature.get("geometry")
        geometryType = geometry.get("type")
        geometryCoords = geometry.get("coordinates")
        properties = feature.get("properties")
        KEY_CODE = properties.get(setting.mbtiles.get("key_name"))

        if geometryType == "Polygon":
            polygon_loop(geometryCoords=geometryCoords, draw=draw, KEY_CODE=KEY_CODE)
        elif geometryType == "MultiPolygon":
            multiPolygon_loop(geometryCoords=geometryCoords, draw=draw, KEY_CODE=KEY_CODE)

    # flip because 
    # Pillow's      axis origin is left upper side
    # x/y/z tile's  axis origin is left lower side
    im_flip = ImageOps.flip(im)
    # set alpha value if needed
    # im_flip.putalpha(128)
    return im_flip


def geojson_file2png_file(
    inputFilePath=None, outputFilePath=None, 
    tile_z=0, tile_x=0, tile_y=0, 
    FIG_SIZE=FIG_SIZE):
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
    z,x,y = int(tile_z),int(tile_x),int(tile_y)
    tileCoordsList = [(z,x,y)]
    geojsonDict = read_tiles(mbtilesPath=inputFilePath, tileCoordsList=tileCoordsList)
    im = geojsonDict2png(geojsonDict[0], FIG_SIZE)
    with open(outputFilePath, mode="wb") as f:
        im.save(fp=f) # イメージ出力


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("filePath is not specified")
    else:
        geojson_file2png_file(
            sys.argv[1], sys.argv[2], # path args
            sys.argv[3], sys.argv[4], sys.argv[5] # z/x/y args
        )