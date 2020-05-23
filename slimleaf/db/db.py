from sqlite3 import connect as sqlite_connect
import ssl

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import WhiteListRoundRobinPolicy
from pymysql import connect, MySQLError

from slimleaf.exceptions import EMPTY_QUERY_MSG, SlimleafException


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


# SQLite3
def get_sqlite3_conx(db_name):
    """Get SQLite3 connection for communicating with the local DB"""
    conn = sqlite_connect(db_name, check_same_thread=False)  # Allows multithread access
    return conn


# Cassandra
def cassandra_connection(user, pw, cluster_host, key, cert_path=None):

    use_ssl = True if cert_path else False

    auth_provider = PlainTextAuthProvider(
        username=user,
        password=pw
    )

    contacts = [cluster_host]

    ssl_options = {
        'ca_certs': cert_path,
        'ssl_version': ssl.PROTOCOL_TLSv1,
        'cert_reqs': ssl.CERT_REQUIRED
    }

    if use_ssl:
        cluster = Cluster(
            contact_points=contacts,
            auth_provider=auth_provider,
            load_balancing_policy=WhiteListRoundRobinPolicy(contacts),
            ssl_options=ssl_options
        )
    else:
        cluster = Cluster(
            contact_points=contacts,
            auth_provider=auth_provider,
            load_balancing_policy=WhiteListRoundRobinPolicy(contacts),
        )

    session = cluster.connect(key)
    return session


def query_result(cxn, qry, args=None, single_row=False, all_fields=True, empty_results=False):
    """Executes a READ-only query against the database (does not COMMIT changes).

    Args:
        cxn (DB-API 2.0 compliant DB connection)
        qry (str): Valid SQL query
        args (dict): (MySQL) Map of names to interpolated values to be substituted during query
             (list): (SQLite3) collection of values to be interpolated into query
        single_row (bool): Whether or not to limit results to the first row
        all_fields (bool): Whether or not to include all fields or only the first
        empty_results (bool): Whether or not empty results are acceptable (raises Exception if not)

    Returns:
        result (list) if all_fields is True
        result (str) if all_fields is False

    """
    args = args or []
    curs = cxn.cursor()
    curs.execute(qry, args)
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
        cxn (DB-API 2.0 compliant DB connection)
        qry (str): Valid SQL query
        args (dict): (MySQL) Map of names to interpolated values to be substituted during query
             (list): (SQLite3) collection of values to be interpolated into query
    Returns:
        last_row_id (cursor.lastrowid): ID of row just inserted
    """
    args = args or []
    curs = cxn.cursor()
    try:
        curs.execute(qry, args)
        cxn.commit()
        return curs.lastrowid
    except MySQLError as e:
        raise SlimleafException(f'Update was unsuccessful') from e
