import sys
import sqlite3
import setting

def fetch_data(KEY_CODE=None, **kwargs):
    """fetch_data from sqlite3 DB
    Parameters
    ----------
    db_path : str
        sqlite3 DB file path
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
        return value from sqlite3
    """
    arg = setting.style_data_sqlite
    db_path, target_col, table_name, idx_col = arg["db_path"], arg["target_col"], arg["table_name"], arg["idx_col"]
    search_str=str(KEY_CODE)
    
    # initialize connection
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # pass str only 0-9,a-z,A-Z
    scrub = lambda string: ''.join( chr for chr in string if chr.isalnum() )
    # create query string by using format
    # we cannot use execute parameter in column/table name
    query_str = (
        "SELECT {0} FROM {1} WHERE {2} = :search"
        .format(scrub(target_col), scrub(table_name), scrub(idx_col))
    )
    c.execute(query_str,({"search": search_str}))
    data = c.fetchone()
    
    conn.close()

    if data is None or data[0] is None:
        return None
    return float(data[0])

if __name__ == "__main__":
    data = fetch_data(
        db_path=sys.argv[1],target_col=sys.argv[2],
        table_name=sys.argv[3],idx_col=sys.argv[4],
        search_str=sys.argv[5]
    )

    print(data)