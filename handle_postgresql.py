import sys
from sqlalchemy import create_engine
import psycopg2
import setting

def fetch_data(target_col, table_name, idx_col, search_str):
    """fetch_data from sqlite3 DB
    Parameters
    ----------
    target_col : str
        column name to fetch
    table_name : str
        table name which has target record
    idx_col : str
        column name which used in where(search)
    search_str :str
        string which is used in search
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
    query_str = (
        "SELECT {0} FROM {1} WHERE {2} = %(search)s"
        .format(target_col, table_name, idx_col)
        # .format(scrub(target_col), scrub(table_name), scrub(idx_col))
    )
    with engine.connect() as con:
        data = con.execute(query_str, search = search_str)
        listed = list(data)
    engine.dispose()
    if listed is None or len(listed) == 0:
        return None
    else:
        return listed[0]

if __name__ == "__main__":
    data = fetch_data(
        target_col=sys.argv[1],table_name=sys.argv[2],
        idx_col=sys.argv[3],search_str=sys.argv[4]
    )

    print(data)