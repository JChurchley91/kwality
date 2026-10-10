from pathlib import Path

from kwality.classes.job import Job
from kwality.classes.test import Test as SqlTest


class FakeCursor:
    def __init__(self) -> None:
        self.rowcount = -1
        self.description = None
        self.statements: list[str] = []
        self.closed = False

    def execute(self, statement: str) -> None:
        self.statements.append(statement)
        if statement.startswith("SELECT"):
            self.description = ("value",)

    def fetchall(self) -> list[tuple[int]]:
        return [(1,), (2,)]

    def close(self) -> None:
        self.closed = True


class FakeConnection:
    def __init__(self) -> None:
        self.cursors: list[FakeCursor] = []

    def cursor(self) -> FakeCursor:
        cursor = FakeCursor()
        self.cursors.append(cursor)
        return cursor


def test_test_executes_each_sql_file_and_prints_row_counts(
    tmp_path: Path, capsys
) -> None:
    sql_folder = tmp_path / "sql"
    sql_folder.mkdir()
    (sql_folder / "02_second.sql").write_text("SELECT 2", encoding="utf-8")
    (sql_folder / "01_first.sql").write_text("SELECT 1", encoding="utf-8")
    connection = FakeConnection()
    test = SqlTest(name="customer-check", sql_folder_path=str(sql_folder))

    assert test.run(connection) == {"01_first.sql": 2, "02_second.sql": 2}
    assert [cursor.statements[0] for cursor in connection.cursors] == [
        "SELECT 1",
        "SELECT 2",
    ]
    assert all(cursor.closed for cursor in connection.cursors)
    assert capsys.readouterr().out.splitlines() == [
        "01_first.sql: 2 rows",
        "02_second.sql: 2 rows",
    ]


def test_job_runs_enabled_tests_in_order(tmp_path: Path) -> None:
    first_folder = tmp_path / "first"
    first_folder.mkdir()
    (first_folder / "check.sql").write_text("SELECT 1", encoding="utf-8")
    disabled_folder = tmp_path / "disabled"
    disabled_folder.mkdir()
    third_folder = tmp_path / "third"
    third_folder.mkdir()
    (third_folder / "check.sql").write_text("SELECT 3", encoding="utf-8")

    connection = FakeConnection()
    job = Job(
        name="customer-quality",
        connection=connection,
        tests=[
            SqlTest(name="null-check", sql_folder_path=str(first_folder)),
            SqlTest(
                name="value-check",
                sql_folder_path=str(disabled_folder),
                enabled=False,
            ),
            SqlTest(name="allowed-values", sql_folder_path=str(third_folder)),
        ],
    )

    assert job.run() == {
        "null-check": {"check.sql": 2},
        "allowed-values": {"check.sql": 2},
    }
    assert [cursor.statements[0] for cursor in connection.cursors] == [
        "SELECT 1",
        "SELECT 3",
    ]
