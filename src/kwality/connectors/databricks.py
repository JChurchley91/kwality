import os

from databricks import sql
from databricks.sql.client import Connection
from dotenv import load_dotenv
from kwality.utils.logger import get_logger

load_dotenv()


def get_databricks_connection() -> Connection:
    """
    Get a connection to the Databricks SQL endpoint
    using environment variables for connection parameters.
    """
    try:
        get_logger(__name__).info("Attempting to connect to Databricks SQL endpoint...")
        connector = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN"),
            use_kernel=True,
        )
        get_logger(__name__).info("Successfully connected to Databricks SQL endpoint.")
        return connector
    except Exception as exception:
        get_logger(__name__).error(
            f"Failed to connect to Databricks SQL endpoint: {exception}"
        )
        raise
