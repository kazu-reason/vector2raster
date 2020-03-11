import sys
from sqlalchemy import create_engine
import psycopg2
import setting

def fetch_data(base_sql, search_str):
    """fetch_data from postgresql DB
    Parameters
    ----------
    base_sql : str
        base sql that base_info(target [col, table], ) is already fulfilled, but must fill search_str(%s)
    search_str : [str, ...]
        string which is used in search placeholders.
        must embed to base_sql.
    
    Deprecated
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
    url = f'postgresql+psycopg2://{setting.PSQL_USER}:{setting.PSQL_PASS}@{setting.PSQL_HOST}:{setting.PSQL_PORT}/{setting.PSQL_DBNAME}'
    engine = create_engine(url)
    
    # pass str only 0-9,a-z,A-Z
    scrub = lambda string: ''.join( chr for chr in string if chr.isalnum() )
    # create query string by using format
    # we cannot use execute parameter in column/table name
    # query_str = (
    #     "SELECT {0} FROM {1} WHERE {2} = %(search)s and delta = %(time)s and date_info = %(latestDate)s"
    #     .format(target_col, table_name, idx_col)
    # )
    with engine.connect() as con:
        data = con.execute(base_sql, *search_str)
        listed = list(data)
    engine.dispose()
    if listed is None or len(listed) == 0:
        return None
    else:
        return listed[0]

if __name__ == "__main__":
    # data = fetch_data(
    #     target_col=sys.argv[1],table_name=sys.argv[2],
    #     idx_col=sys.argv[3],search_str=sys.argv[4]
    # )
    data = fetch_data(
        base_sql=sys.argv[1], search_str=sys.argv[2]
    )

    print(data)