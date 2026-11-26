# Business API

This service is the FastAPI business API package `omnicore_api`. It currently provides liveness/readiness checks and the shared PostgreSQL session and migration foundation; it does not implement product APIs or authentication.

## Configuration

Set `DATABASE_URL` in the process environment or in a local `.env` file. `DB_CONNECT_TIMEOUT_SECONDS` defaults to `3` and accepts values from `1` to `30`. The value in `.env.example` is a local Compose example; use a host appropriate to the environment where the service runs. The database URL is treated as secret configuration and is not returned by health checks.

## Run and verify

From the repository root, install this package with its development tools using `uv sync --package omnicore-api --extra dev`. Then run `uv run --package omnicore-api --extra dev uvicorn omnicore_api.main:app --reload`.

Run focused tests with `uv run --package omnicore-api --extra dev pytest apps/api/tests` and lint with `uv run --package omnicore-api --extra dev ruff check apps/api/omnicore_api apps/api/tests`.

Apply approved migrations with `uv run --package omnicore-api --extra dev alembic -c apps/api/alembic.ini upgrade head`. The migration directory is intentionally empty until an application schema is approved.
