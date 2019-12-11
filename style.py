import random
from pandas import read_csv
import handle_sqlite
import setting
    
def get_color_from_csv(KEY_CODE=None):
    if setting.csvHeaders is None:
        csvHeaders = ["id","lng","lat","val","empty"]
    else:
        csvHeaders = setting.csvHeaders
    src = read_csv(setting.csvFilePath, names=csvHeaders)
    value = float(src.query("id == {}".format(KEY_CODE)).loc[:,"val"])
    
    return setting.thresholds_function(value=value)

def get_color_from_sqlite(KEY_CODE=None):
    value = handle_sqlite.fetch_data(
        **setting.style_data_sqlite,
        search_str=str(KEY_CODE)
    )

    if value is None:
        return (0,0,0)
    value = float(value[0])

    return setting.thresholds_function(value=value)

def get_random_color(KEY_CODE):
    rand_tuple = (
        55+random.randint(0,200),
        55+random.randint(0,200),
        55+random.randint(0,200)
    )

    return rand_tuple

if __name__ == "__main__":
    KEY_CODE = input().rstrip("\n")
    print(get_color_from_csv(KEY_CODE))
    print(get_color_from_sqlite(KEY_CODE))