from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from omnicore_api.api.health import router as health_router
from omnicore_api.api.v1 import router as v1_router
from omnicore_api.core.config import Settings, get_settings
from omnicore_api.core.database import build_engine, build_session_factory


def create_app(settings: Settings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        active_settings = settings or get_settings()
        engine = build_engine(active_settings)
        app.state.settings = active_settings
        app.state.engine = engine
        app.state.session_factory = build_session_factory(engine)
        try:
            yield
        finally:
            engine.dispose()

    application = FastAPI(
        title="OMNICORE AI Business API",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.include_router(health_router)
    application.include_router(v1_router, prefix="/api/v1")
    return application


app = create_app()
