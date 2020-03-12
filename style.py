import random
from pandas import read_csv
import handle_sqlite
import handle_postgresql
import setting
    
def get_color_from_csv(KEY_CODE=None):
    if setting.csvHeaders is None:
        csvHeaders = ["id","lng","lat","val","empty"]
    else:
        csvHeaders = setting.csvHeaders
    src = read_csv(setting.csvFilePath, names=csvHeaders)
    value = float(src.query("id == {}".format(KEY_CODE)).loc[:,"val"])
    
    return setting.thresholds_function(value=value)


def get_color_from_sqlite(KEY_CODE=None, **kwargs):
    value = handle_sqlite.fetch_data(
        **setting.style_data_sqlite,
        search_str=str(KEY_CODE),
    )

    if value is None or value[0] is None:
        return None
    value = float(value[0])

    return setting.style_function(value=value)


def get_color_from_postgresql(KEY_CODE_LIST=None, **kwargs):
    search_str = {"KEY_CODE_LIST":KEY_CODE_LIST}
    # keycode以外の条件を追加(optional)
    search_str.update(kwargs)
    # 使用するSQLを指定(SQL文が配列に格納されていることを想定)
    sql_num = kwargs.get("sql_num", 0)
    # print(setting.style_data_postgresql.get("base_sqls"))
    value = handle_postgresql.fetch_data(
        setting.style_data_postgresql.get("base_sqls")[sql_num],
        search_str=search_str,
    )

    # if value is None or value[0] is None:
    #     return None
    # value = float(value[0])

    # return setting.style_function(value=value)
    return value


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
