from unittest.mock import MagicMock, patch

from pytest import raises
from pymysql import MySQLError

from slimleaf.db import get_mysql_connection, query_result, update_db
from slimleaf.exceptions import SlimleafException


test_conn_data = {
        'host': 'testhost',
        'rw-user': 'testuser',
        'rw-password': 'testpass',
        'database': 'testdb'
    }

fetchone_result = ['fetchone result']
fetchall_result = ['fetchall result']
empty_results = []
query = 'dummy query'


@patch('slimleaf.db.db.connect')
def test_get_connection(_mock_conn):
    success_val = 'success'
    _mock_conn.return_value = success_val

    cxn = get_mysql_connection(test_conn_data)
    assert cxn == success_val


@patch('slimleaf.db.db.connect')
def test_query_result(_mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = fetchone_result
    mock_cursor.fetchall.return_value = fetchall_result

    # mock connection().cursor()
    _mock_conn.return_value.cursor.return_value = mock_cursor

    cxn = get_mysql_connection(test_conn_data)
    # single_row=False should return fetchall, all_fields should return entire list
    result = query_result(cxn, qry=query, single_row=False, all_fields=True)
    assert result == fetchall_result

    # single_row=True should return fetchone, all_fields=False should return first index of list
    result = query_result(cxn, qry=query, single_row=True, all_fields=False)
    assert result == fetchone_result[0]


@patch('slimleaf.db.db.connect')
def test_empty_result_exc(_mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = empty_results
    _mock_conn.return_value.cursor.return_value = mock_cursor

    cxn = get_mysql_connection(test_conn_data)

    with raises(SlimleafException) as empty_results_exc:
        query_result(cxn, qry=query, single_row=True, all_fields=True)
    assert 'query was empty' in str(empty_results_exc.value)


@patch('slimleaf.db.db.connect')
def test_update_db(_mock_conn):
    mock_cursor = MagicMock()
    _mock_conn.return_value.cursor.return_value = mock_cursor

    cxn = get_mysql_connection(test_conn_data)

    update_db(cxn=cxn, qry=query, args={'testarg': 'value'})
    cxn.commit.assert_called_once()


@patch('slimleaf.db.db.connect')
def test_update_error(_mock_conn):
    mock_cursor = MagicMock()
    _mock_conn.return_value.cursor.return_value = mock_cursor

    cxn = get_mysql_connection(test_conn_data)
    mock_cursor.execute.side_effect = [MySQLError]

    with raises(SlimleafException) as mysql_exc:
        update_db(cxn=cxn, qry=query)
    assert 'Update was unsuccessful' in str(mysql_exc.value)
