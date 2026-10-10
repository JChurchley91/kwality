# Kwality

Kwality is a Python project for running SQL-based data-quality checks against
Databricks SQL. A check consists of one or more `.sql` files: each statement is
executed in order and its result row count is printed. The included examples
look for `NULL` values in the raw customers and products tables.

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)
- A Databricks SQL workspace and a token with permission to connect and query
  the tables referenced by the checks (needed only for live Databricks runs)

## Set up

Clone the repository and change into its directory:

```bash
git clone https://github.com/JChurchley91/kwality.git
cd kwality
```

Install the project and its locked dependencies into a uv-managed environment:

```bash
uv sync
```

`uv sync` creates `.venv` if needed and installs the project dependencies from
`uv.lock`. To update the environment after dependency changes, run `uv sync`
again.

## Databricks configuration

The connector loads environment variables from a `.env` file in the current
working directory. Create `.env` with the details for your Databricks SQL
warehouse:

```dotenv
DATABRICKS_SERVER_HOSTNAME=<workspace-hostname>
DATABRICKS_HTTP_PATH=<warehouse-http-path>
DATABRICKS_TOKEN=<personal-access-token>
```

Use the hostname and HTTP path shown in the warehouse's connection details.
Keep the token secret; `.env` is ignored by Git and should not be committed.

The example SQL files reference `dbt.raw.raw_customers` and
`dbt.raw.raw_products`; make sure these tables are available to the configured
identity, or adjust the SQL for your workspace.

## Run the example checks

From the repository root, run:

```bash
uv run python main.py
```

This starts the scheduler and registers a cron job that runs the raw data-quality
checks on a timer. The current scheduler configuration registers a job named
`raw_tests` on the cron expression `*/30 * * * *`, which triggers every 30
minutes. When the job fires, it connects to Databricks, runs the customer and
product checks, and closes the connection. A nonzero row count means the query
found rows matching that check (for example, customers with a null `ID` or
`NAME`).

The scheduler runs in a blocking loop while the process is alive, so the app
continues running until you stop it with Ctrl+C. This makes it suitable for
scheduled jobs that should keep polling on a cron cadence without needing a
separate worker process.

## Scheduler usage

The scheduler wrapper lives in `src/kwality/utils/scheduler.py` and is a thin
wrapper around APScheduler's `BackgroundScheduler`.

```python
from kwality.utils.scheduler import Scheduler

scheduler = Scheduler(timezone="UTC")
scheduler.add_job(my_job, "*/5 * * * *", job_id="my-job")
scheduler.start()
```

This adds a cron-triggered job to the scheduler using a standard 5-field crontab
string. Jobs are configured with:

- `coalesce=True` to collapse missed runs into a single execution
- `max_instances=1` to prevent overlapping runs of the same job
- `misfire_grace_time=60` to allow a small recovery window for delayed runs

Jobs are scheduled from `main.py` by calling `scheduler.add_job(...)` before
entering the infinite loop. The example currently schedules the Databricks raw
check job via `run_raw_tests`, which can be replaced with any callable you want
to run on cron timings.

## Run tests

Run the local unit tests without contacting Databricks:

```bash
uv run pytest src/kwality/tests/test_classes.py src/kwality/tests/test_utils.py
```

The connector test uses live Databricks credentials and makes a real query.
Run it separately when the `.env` configuration is available:

```bash
uv run pytest src/kwality/tests/test_connectors.py
```

To run all tests, including the live connector test:

```bash
uv run pytest
```

## Project layout

```text
src/kwality/
  classes/       SQL-backed Test and ordered Job abstractions
  connectors/    Databricks SQL connection helper
  tests/         Unit tests, including the live connector test
  utils/         Logging, SQL helpers, and cron scheduler wrapper
tests/raw/       Example customer and product check definitions
sql/raw/         SQL statements executed by the example checks
main.py          Example scheduler entry point for cron-triggered jobs
```

`Test` executes the `.sql` files in its configured folder in filename order.
`Job` runs a sequence of enabled tests and returns their per-file row counts.
The scheduler wrapper adds recurring cron-based execution without requiring an
external job queue or scheduler service.

## Development checks

Ruff and ty are included in the project dependencies. You can run them with:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
```

The installed `kwality` command currently invokes the package's placeholder
`main()` function, which prints a greeting. Use `uv run python main.py` to run
the Databricks example checks.