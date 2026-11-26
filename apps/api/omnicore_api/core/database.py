from collections.abc import Iterator

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from omnicore_api.core.config import Settings


def build_engine(settings: Settings) -> Engine:
    database_url = settings.database_url.get_secret_value()
    parsed_url = make_url(database_url)
    options: dict[str, object] = {"pool_pre_ping": True}

    if parsed_url.get_backend_name() == "postgresql":
        options["connect_args"] = {
            "connect_timeout": settings.db_connect_timeout_seconds,
        }
    elif parsed_url.get_backend_name() == "sqlite" and parsed_url.database in (
        None,
        "",
        ":memory:",
    ):
        options["connect_args"] = {"check_same_thread": False}
        options["poolclass"] = StaticPool

    return create_engine(parsed_url, **options)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db(request: Request) -> Iterator[Session]:
    session: Session = request.app.state.session_factory()
    try:
        yield session
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()
