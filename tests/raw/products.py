from dataclasses import dataclass

from databricks.sql.client import Connection

from kwality.classes.test import Test


@dataclass
class TestProducts(Test):
    name: str = "TestProducts"
    sql_folder_path: str = "sql/raw/products"
    description: str = "Check the raw products table for null values"
    enabled: bool = True
    connection: Connection | None = None

    def run(self) -> dict[str, int | None]:
        if self.connection is None:
            raise ValueError("A Databricks connection is required to run this test.")
        return super().run(self.connection)
