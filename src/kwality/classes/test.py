from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kwality.utils.sql import execute_sql


@dataclass
class Test:
    """A SQL-backed data-quality check that writes its results using SQL."""

    name: str
    sql: str
    description: str = ""
    enabled: bool = True

    def build_sql(self) -> str:
        """Return the SQL statement that performs and records this check."""
        return self.sql

    def run(self, connection: Any) -> int | None:
        """Execute this test's SQL and return the connector's row count."""
        if connection is None:
            raise ValueError("A SQL connection is required to run a test.")
        if not self.enabled:
            return None

        statement = self.build_sql()
        if not statement.strip():
            raise ValueError(f"Test '{self.name}' did not provide a SQL statement.")

        return execute_sql(connection, statement)
