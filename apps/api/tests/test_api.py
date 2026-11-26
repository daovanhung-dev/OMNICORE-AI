from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi import FastAPI
from fastapi.testclient import TestClient
from omnicore_api.core.config import Settings
from omnicore_api.core.database import get_db
from omnicore_api.core.models import Base
from omnicore_api.main import create_app
from sqlalchemy.exc import OperationalError
from starlette.requests import Request


def test_health_live_is_independent_of_database() -> None:
    app = create_app(Settings(database_url="sqlite:///:memory:"))

    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "api"}


def test_health_ready_executes_database_probe() -> None:
    app = create_app(Settings(database_url="sqlite:///:memory:"))

    with TestClient(app) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "api"}


def test_health_ready_returns_safe_503_when_database_probe_fails() -> None:
    failing_engine = SimpleNamespace(
        connect=lambda: (_ for _ in ()).throw(
            OperationalError("connect", {}, RuntimeError("private-database-detail"))
        ),
        dispose=lambda: None,
    )
    settings = Settings(database_url="postgresql+psycopg://user:secret@127.0.0.1/db")
    app = create_app(settings)

    with patch("omnicore_api.main.build_engine", return_value=failing_engine), TestClient(app) as client:
        response = client.get("/health/ready")
        liveness = client.get("/health/live")

    assert response.status_code == 503
    assert response.json() == {"status": "not_ready", "service": "api"}
    assert "private-database-detail" not in response.text
    assert "secret" not in response.text
    assert liveness.status_code == 200


def test_settings_mask_database_url_and_validate_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:secret@localhost/db")
    monkeypatch.setenv("DB_CONNECT_TIMEOUT_SECONDS", "4")

    settings = Settings()

    assert settings.db_connect_timeout_seconds == 4
    assert "secret" not in repr(settings)
    with pytest.raises(ValueError):
        Settings(database_url="sqlite:///:memory:", db_connect_timeout_seconds=0)


def test_database_dependency_rolls_back_errors_and_always_closes() -> None:
    class FakeSession:
        rolled_back = False
        closed = False

        def rollback(self) -> None:
            self.rolled_back = True

        def close(self) -> None:
            self.closed = True

    session = FakeSession()
    app = FastAPI()
    app.state.session_factory = lambda: session
    request = Request({"type": "http", "app": app})
    dependency = get_db(request)

    assert next(dependency) is session
    with pytest.raises(RuntimeError, match="request failed"):
        dependency.throw(RuntimeError("request failed"))

    assert session.rolled_back
    assert session.closed


def test_alembic_is_configured_without_domain_migrations() -> None:
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    scripts = ScriptDirectory.from_config(config)

    assert scripts.get_heads() == []
    assert Base.metadata.tables == {}
