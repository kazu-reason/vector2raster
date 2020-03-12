import sys
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql
import setting

def fetch_data(KEY_CODE_LIST=None, **kwargs):
    """fetch_data from postgresql DB
    Parameters
    ----------
    KEY_CODE_LIST : [str]
        target key code list
    sql_num : int
        the number which specify base sql
    
    Deprecated
    base_sql : str
        base sql that base_info(target [col, table], ) is already fulfilled, but must fill search_str(%s)
    search_str : [str, ...]
        string which is used in search placeholders.
        must embed to base_sql.
    target_col : str
        column name to fetch
    table_name : str
        table name which has target record
    idx_col : str
        column name which used in where(search)

    Returns
    -------
    (str,)
        return value from postgreSQL
    """
    # initialize connection
    url = f'postgresql://{setting.PSQL_USER}:{setting.PSQL_PASS}@{setting.PSQL_HOST}:{setting.PSQL_PORT}/{setting.PSQL_DBNAME}'
    
    search_str = {"KEY_CODE_LIST":KEY_CODE_LIST}
    # keycode以外の条件を追加(optional)
    search_str.update(kwargs)
    # 使用するSQLを指定(SQL文が配列に格納されていることを想定)
    sql_num = kwargs.get("sql_num", 0)
    base_sql = setting.style_data_postgresql.get("base_sqls")[sql_num]

    with psycopg2.connect(url) as con:
        with con.cursor('vector2raster') as cur:
            cur.execute(sql.SQL(base_sql).format(sql.Identifier(search_str.get("table_name"))), search_str)
            res = cur.fetchall()
            return res

if __name__ == "__main__":
    # data = fetch_data(
    #     target_col=sys.argv[1],table_name=sys.argv[2],
    #     idx_col=sys.argv[3],search_str=sys.argv[4]
    # )
    data = fetch_data(
        base_sql=sys.argv[1], search_str=sys.argv[2]
    )

    print(data)