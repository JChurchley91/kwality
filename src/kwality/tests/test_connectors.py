from kwality.connectors.databricks import get_databricks_connection


def test_databricks_connection():
    """
    Test the connection to the Databricks SQL endpoint and
    verify that the catalogs can be queried successfully.
    """
    connection = get_databricks_connection()
    assert connection is not None
    assert connection.cursor() is not None

    with connection.cursor() as cursor:
        cursor.execute("select * from workspace.information_schema.catalogs")
        result = cursor.fetchall()

    assert len(result) >= 1
