from kwality.classes.job import Job
from kwality.classes.test import Test as SqlTest


class FakeCursor:
    def __init__(self, rowcount: int = 1) -> None:
        self.rowcount = rowcount
        self.statements: list[str] = []
        self.closed = False

    def execute(self, statement: str) -> None:
        self.statements.append(statement)

    def close(self) -> None:
        self.closed = True


class FakeConnection:
    def __init__(self) -> None:
        self.cursors: list[FakeCursor] = []

    def cursor(self) -> FakeCursor:
        cursor = FakeCursor()
        self.cursors.append(cursor)
        return cursor


def test_test_executes_sql_and_closes_cursor() -> None:
    connection = FakeConnection()
    test = SqlTest(name="null-check", sql="INSERT INTO dq_results SELECT 1")

    assert test.run(connection) == 1
    assert connection.cursors[0].statements == [
        "INSERT INTO dq_results SELECT 1"
    ]
    assert connection.cursors[0].closed


def test_job_runs_enabled_tests_in_order() -> None:
    connection = FakeConnection()
    job = Job(
        name="customer-quality",
        connection=connection,
        tests=[
            SqlTest(name="null-check", sql="INSERT INTO results SELECT 1"),
            SqlTest(
                name="value-check",
                sql="INSERT INTO results SELECT 2",
                enabled=False,
            ),
            SqlTest(name="allowed-values", sql="INSERT INTO results SELECT 3"),
        ],
    )

    assert job.run() == {"null-check": 1, "allowed-values": 1}
    assert [cursor.statements[0] for cursor in connection.cursors] == [
        "INSERT INTO results SELECT 1",
        "INSERT INTO results SELECT 3",
    ]
