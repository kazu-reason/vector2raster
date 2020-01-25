from math import isclose
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PSQL_PASS = os.environ.get("PSQL_PASS")
PSQL_HOST = os.environ.get("PSQL_HOST")
PSQL_PORT = os.environ.get("PSQL_PORT")
PSQL_USER = os.environ.get("PSQL_USER")
PSQL_DBNAME = os.environ.get("PSQL_DBNAME")

# This file is setting example
# Please copy this file as setting.py and edit to suit your project

#####################
# setting for STYLE #
#####################
style_format = "level"
# style_function get (value:int) and return ((R,G,B):(int,int,int))
style_function = thresholds_function

thresholds_list = [0,0.5,1,5,10]
rgba_style_list = [
    (0,0,0),(50,174,183),(50,67,183),
    (84,183,50),(224,54,27)]
def thresholds_function(value = 0):
    if len(thresholds_list) != len(rgba_style_list):
        print("style_setting is incorrect")
        return (0,0,0)
    if isclose(value, 0.0):
        return (0,0,0)
    for idx, threshold in enumerate(thresholds_list):
        if threshold > value: # find proper style threshold in list
            return rgba_style_list[idx]
    
    # return initial style for outrange value
    idx = 0
    return rgba_style_list[idx]

###########################
# setting for DATA SOURCE #
###########################

# mbtiles source
mbtiles = {
    "path": "mbtiles_path",
    "key_name": "KEY_CODE_NAME_TO_LINK_YOUR_DATA"
}


# geojson source
GEOJSON_SRC_URL="http://localhost:8080/your_geojson_data/{0}/{1}/{2}.geojson"


# Style source
color_src = "postgresql"
# sqlite
style_data_sqlite = {
    "db_path": "sqlite_file_path", "target_col": "col_name_which_you_want_to_get", 
    "table_name": "target_table_name", "idx_col": "col_name_which_has_key_code"
}
# postgresql
style_data_postgresql = {
    "target_col": "val", 
    "table_name": "layer_value_1", "idx_col": "mesh_code"
}
# csv
csvFilePath="path_to_your.csv"
csvHeaders=["id","lng","lat","val","empty"] # example

