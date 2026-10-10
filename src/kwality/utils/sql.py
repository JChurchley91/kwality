from __future__ import annotations

from typing import Any


def execute_sql(connection: Any, statement: str) -> int | None:
    """Execute one statement using the DB-API
    cursor shared by SQL connectors."""
    cursor = connection.cursor()
    try:
        cursor.execute(statement)
        if cursor.description is not None:
            return len(cursor.fetchall())

        rowcount = cursor.rowcount
        return rowcount if isinstance(rowcount, int) else None
    finally:
        cursor.close()
