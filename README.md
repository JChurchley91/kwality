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

This connects to Databricks, runs the customer and product checks under
`sql/raw/`, prints the number of rows returned by each SQL file, and closes the
connection. A nonzero row count means the query found rows matching that check
(for example, customers with a null `ID` or `NAME`).

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
  utils/         SQL execution and logging helpers
tests/raw/       Example customer and product check definitions
sql/raw/         SQL statements executed by the example checks
main.py          Example runner for the raw checks
```

`Test` executes the `.sql` files in its configured folder in filename order.
`Job` runs a sequence of enabled tests and returns their per-file row counts.

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