import sys
from gzip import decompress
import mapbox_vector_tile as mvt
from pymbtiles import MBtiles, TileCoordinate

def read_tiles(mbtilesPath=None, tileCoordsList=None):
    """Read tiles from mbtiles
    Read tiles from mbtiles in XYZ format.
    Need file path and list of tileCoords( tuple(z,x,y) ).
    Function return list which has dict(geojson format).

    Parameters
    ----------
    mbtilesPath : str
        path of mbtiles
    tileCoordsList : list
        [(z,x,y), ...]

    Returns
    -------
    list
        [dict, ...]

    """

    # func_pbf2dict = pbf2dict
    # func_decompress_pbf = decompress_pbf
    # func_flip_y = flip_y
    tile_data_list = []
    # TODO: refactoring
    for coords in tileCoordsList:
        z, x, y = coords
        with MBtiles(mbtilesPath) as db:
            tile_data_list.append(
                pbf2dict(
                    decompress_pbf(
                        db.read_tile(
                            z=z,
                            x=x,
                            # convert y coord to xyz style
                            y=flip_y(
                                y=y,
                                z=z
                            )
                        )
                    )
                )
            )

    return tile_data_list


def decompress_pbf(pbf):
    try:
        decompressed = decompress(pbf)
    except OSError as e:
        pass

    return decompressed


def flip_y(y, z):
    '''Convert XYZ / TMS y coordinate
    Convert XYZ / TMS y coordinate between them

    Parameters
    ----------
    y : int
        tile y coords
    z : int
        tile z coords

    Returns
    -------
    int
        Converted y coordinate
            
    '''
    power_of_two = (
        [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024,
        2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144,
        524288, 1048576, 2097152, 4194304, 8388608, 16777216])

    # same as (2 ** z) - y - 1
    return power_of_two[z] - y - 1


pbf2dict = lambda pbf: mvt.decode(pbf)

def get_tileCoords(mbtilesPath=None):
    
    with MBtiles(mbtilesPath) as db:
        list_tiles = db.list_tiles()

    return list_tiles

# def get_dict_from_mbtiles(mbtilesPath=None, tileCoordsList=None):
#     tile_data_list = read_tiles(mbtilesPath=mbtilesPath, tileCoordsList=tileCoordsList)
    
if __name__ == "__main__":
    print(get_tileCoords(sys.argv[1]))

