from pymysql import connect, MySQLError

from slimleaf.exceptions import SlimleafException


EMPTY_QUERY_MSG = "Expected results but query was empty"


# MySQL
def get_mysql_connection(cxn_data):
    """Retrieve a pymysql connection

    Args:
        cxn_data (dict): map of connection information: host, rw-user, rw-password, database

    Returns:
        pymysql.connections.Connection

    """
    return connect(
        host=cxn_data['host'],
        user=cxn_data['rw-user'],
        password=cxn_data['rw-password'],
        db=cxn_data['database'])


def query_result(cxn, qry, args=None, single_row=False, all_fields=True, empty_results=False):
    """Executes a READ-only query against the database (does not COMMIT changes).

    Args:
        cxn (pymysql.connections.Connection)
        qry (str): Valid MySQL query
        args (dict): Map of names to interpolated values to be substituted during query
        single_row (bool): Whether or not to limit results to the first row
        all_fields (bool): Whether or not to include all fields or only the first
        empty_results (bool): Whether or not empty results are acceptable (raises Exception if not)

    Returns:
        result (list) if all_fields is True
        result (str) if all_fields is False

    """
    curs = cxn.cursor()
    curs.execute(qry, args=args)
    if single_row:
        result = curs.fetchone()
    else:
        result = curs.fetchall()
    if not result and not empty_results:
        raise SlimleafException(EMPTY_QUERY_MSG)
    else:
        return result if all_fields else result[0]


def update_db(cxn, qry, args=None):
    """Executes a WRITE query against the database, including a COMMIT.

    Args:
        cxn (pymysql.connections.Connection)
        qry (str): Valid MySQL query
        args (dict): Map of names to interpolated values to be substituted during query

    Returns:
        (pymysql.cursors.Cursor.lastrowid): ID of row just inserted
        """
    curs = cxn.cursor()
    try:
        curs.execute(qry, args=args)
        cxn.commit()
        return curs.lastrowid
    except MySQLError as e:
        raise SlimleafException(f'Update was unsuccessful') from e
