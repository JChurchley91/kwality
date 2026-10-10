from kwality.connectors.databricks import get_databricks_connection
from kwality.utils.logger import get_logger
from tests.raw.customers import TestCustomers
from tests.raw.products import TestProducts


def run_raw_tests() -> None:
    get_logger(__name__).info("Running raw tests.")
    connection = get_databricks_connection()
    try:
        TestCustomers(connection=connection).run()
        TestProducts(connection=connection).run()
        get_logger(__name__).info("Finished running raw tests.")
    finally:
        connection.close()
