from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from kwality.classes.test import Test


@dataclass
class Job:
    """An ordered collection of SQL-backed data-quality tests."""

    name: str
    connection: Any
    tests: list[Test] = field(default_factory=list)
    description: str = ""
    enabled: bool = True

    def validate(self) -> None:
        if self.connection is None:
            raise ValueError("A SQL connection is required to run a job.")
        if not self.tests:
            raise ValueError("A job must contain at least one test.")

    def run(self) -> dict[str, dict[str, int | None]]:
        """Run enabled tests in order and return row counts by test and SQL file."""
        if not self.enabled:
            return {}

        self.validate()
        results: dict[str, dict[str, int | None]] = {}
        for test in self.tests:
            if test.enabled:
                results[test.name] = test.run(self.connection)
        return results

    def execute(self) -> dict[str, dict[str, int | None]]:
        """Validate and run this job."""
        return self.run()
