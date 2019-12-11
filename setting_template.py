from math import isclose

# This file is setting example
# Please copy this file as setting.py and edit to suit your project

#####################
# setting for STYLE #
#####################
style_format = "level"
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
mbtiles_path="mbtiles_path"


# geojson source
GEOJSON_SRC_URL="http://localhost:8080/your_geojson_data/{0}/{1}/{2}.geojson"


# Style source
# sqlite
style_data_sqlite = {
    "db_path": "sqlite_file_path", "target_col": "col_name_which_you_want_to_get", 
    "table_name": "target_table_name", "idx_col": "col_name_which_has_key_code"
}
# csv
csvFilePath="path_to_your.csv"
csvHeaders=["id","lng","lat","val","empty"] # example

