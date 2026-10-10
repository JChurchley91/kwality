from kwality.connectors.databricks import get_databricks_connection
from tests.raw.customers import TestCustomers
from tests.raw.products import TestProducts

connection = get_databricks_connection()

try:
    test_raw_customers = TestCustomers(connection=connection).run()
    test_raw_products = TestProducts(connection=connection).run()
finally:
    connection.close()
