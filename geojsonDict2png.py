import sys
import itertools
from math import pi, e, atan
from PIL import Image, ImageDraw, ImageOps
import shapely
from handle_mbtiles import read_tiles
from style import get_color_from_sqlite, get_color_from_postgresql, get_random_color
import setting

FIG_SIZE = 256

def geojsonDict2png(geojsonDict=None, FIG_SIZE=FIG_SIZE, **kwargs):
    """create png data from geojson data

    create png data from geojson data(does not use geopandas)

    Parameters
    ----------
    geojsonDict : dict
        source data for creating raster image
    FIG_SIZE : int
        raster image size
    value_src : str(default:'random')
        decide to use random coloring or specify DB to get value

    Returns
    -------
    PIL.Image.Image
        raster image data(Pillow format)
            
    """

    # initialize
    im = Image.new("RGBA", (FIG_SIZE, FIG_SIZE), (255,255,255,0))
    draw = ImageDraw.Draw(im)
    
    # return all transparent layer for empty dataset
    if len(geojsonDict) == 0:
        return im

    dictContent = geojsonDict.get(list(geojsonDict.keys())[0])
    features = dictContent.get("features")
    extent = dictContent.get("extent")
    DPI = FIG_SIZE / extent # dot per extent
    value_src = setting.value_src
    if value_src == "sqlite":
        from handle_sqlite import fetch_data
    elif value_src in "postgresql":
        from handle_postgresql import fetch_data
    
    if value_src in ["sqlite", "postgresql"]:
        func_get_color = setting.style_function
    else:
        func_get_color = get_random_color
    

    def position_in_image(geom_x, geom_y):
        image_x = geom_x * DPI
        image_y = geom_y * DPI

        return (image_x, image_y)
    

    def polygon_loop(geometryCoords=None, draw=None, color=None):
        func_PII = position_in_image

        for coords_1 in geometryCoords:
            image_xy_list = []
            for coords_2 in coords_1:
                x,y = coords_2
                image_coords = func_PII(x,y)
                image_xy_list.append(image_coords)

            # draw polygons from image_xy_list
            if color is not None:
                draw.polygon(xy=image_xy_list, fill=color)
    
    
    def multiPolygon_loop(geometryCoords=None, draw=None, color=None):
        func_PII = position_in_image

        for coords_1 in geometryCoords:
            for coords_2 in coords_1:
                image_xy_list = []
                for coords_3 in coords_2:
                    x,y = coords_3
                    image_coords = func_PII(x,y)
                    image_xy_list.append(image_coords)

                # draw polygons from image_xy_list
                if color is not None:
                    draw.polygon(xy=image_xy_list, fill=color)
    
    geometry_dict = {}
    KEY_CODE_list = []
    for feature in features:
        geometry = feature.get("geometry")
        geometryType = geometry.get("type")
        geometryCoords = geometry.get("coordinates")
        properties = feature.get("properties")
        KEY_CODE = str(properties.get(setting.mbtiles.get("key_name")))
        geometry_dict[KEY_CODE] = (geometryType, geometryCoords)
        KEY_CODE_list.append(KEY_CODE)

    key_code_list_len = len(KEY_CODE_list)
    # SQLのANY対象にできる配列の要素数上限に対応するための処理
    array_limit = 1000
    if key_code_list_len < 1001:
        rows = fetch_data(KEY_CODE_list, **kwargs) # return [(KEY_CODE, val),]
    else:
        rows = []
        for i in range(0,key_code_list_len//array_limit):
            i = i*array_limit
            rows.extend(fetch_data(KEY_CODE_list[i:i+array_limit], **kwargs)) # return [(KEY_CODE, val),]
        if key_code_list_len%array_limit != 0:
            rows.extend(fetch_data(KEY_CODE_list[i+array_limit:], **kwargs)) # return [(KEY_CODE, val),]

    for row in rows:
        geometryType, geometryCoords = geometry_dict[row[0]]
        color = func_get_color(row[1])
        if geometryType == "Polygon":
            polygon_loop(geometryCoords=geometryCoords, draw=draw, color=color)
        elif geometryType == "MultiPolygon":
            multiPolygon_loop(geometryCoords=geometryCoords, draw=draw, color=color)

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
    FIG_SIZE=FIG_SIZE, **kwargs):
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
    geojsonDict = read_tiles(mbtilesPath=inputFilePath, tileCoordsList=tileCoordsList, **kwargs)
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