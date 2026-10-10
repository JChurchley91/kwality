from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kwality.utils.sql import execute_sql


@dataclass
class Test:
    """A SQL-backed data-quality check that writes its results using SQL."""

    name: str
    sql_folder_path: str
    description: str = ""
    enabled: bool = True

    def build_sql(self) -> list[Path]:
        """Return the SQL files in this test's folder in stable order."""
        sql_folder = Path(self.sql_folder_path)
        if not sql_folder.is_dir():
            raise FileNotFoundError(
                f"SQL folder for test '{self.name}' does not exist: {sql_folder}"
            )

        sql_files = sorted(sql_folder.glob("*.sql"))
        if not sql_files:
            raise ValueError(
                f"No .sql files found for test '{self.name}' in {sql_folder}."
            )
        return sql_files

    def run(self, connection: Any) -> dict[str, int | None]:
        """Execute each SQL file and print and return its row count."""
        if connection is None:
            raise ValueError("A SQL connection is required to run a test.")
        if not self.enabled:
            return {}

        row_counts = {}
        for sql_file in self.build_sql():
            statement = sql_file.read_text(encoding="utf-8")
            if not statement.strip():
                raise ValueError(
                    f"SQL file for test '{self.name}' is empty: {sql_file}"
                )

            row_count = execute_sql(connection, statement)
            print(f"{sql_file.name}: {row_count} rows")
            row_counts[sql_file.name] = row_count
        return row_counts
